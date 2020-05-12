from __future__ import division
import numpy as np
import logging
from beyourself.core.util import assert_monotonic, assert_vector, epoch_to_datetime
from scipy import signal


logger = logging.getLogger(__name__)


def moving_variance_threshold(df, window_minutes=5, threshold=0):
    '''
    Remove static time of usage based on the moving variance
    of ambient light and quaternion
    '''
    logger.info("N sample before removal: {}".format(df.shape[0]))

    df = df.copy()
  

    varAmbient = df['ambient'].rolling(center=True, window=20*60*window_minutes).std()
    varLf = df['leanForward'].rolling(center=True, window=20*60*window_minutes).std()

    out = df.loc[(varAmbient + varLf) > threshold]

    logger.info("N sample after removal: {}".format(out.shape[0]))

    return out



def peak_detection(arr, min_prominence=0.05):
    '''
    Prominence based
    '''
    peaksIndex = signal.find_peaks(arr, threshold=2, prominence=min_prominence)[0].astype(int)

    return peaksIndex


def get_periodic_stat(a):
    '''
    Given a sequence, find its periodicity statistics

    Returns
    -------

    stat: dictionary
        pmin
        pmax
        eps
        length

    '''

    assert_vector(a)
    assert_monotonic(a)

    stat = {}

    diff = []
    for i in range(len(a) - 1):
        diff.append(a[i + 1] - a[i])

    stat['pmin'] = min(diff)
    stat['pmax'] = max(diff)
    stat['eps'] = stat['pmax'] / stat['pmin'] - 1
    stat['start'] = epoch_to_datetime(a[0])
    stat['end'] = epoch_to_datetime(a[-1])
    stat['length'] = len(a)

    return stat


def periodic_subsequence(peaksIndex, peaksTime, min_length=5, max_length=100, eps=0.15, alpha=0.1, low=500, high=1000):
    '''
    Find periodic subsequences from an array of timestamp, and values

    Parameters
    ----------

    peaksIndex: list of peak index
    peaks_time: list of timestamps
    min_length: minimum length of the subsequence
    max_length: maximum length of the subsequence
    eps: periodicity attribute
    alpha: error bound percentage of upper margin
    low: lower bound for series of p_min
    high: upper bound for series of p_max

    Returns
    -------

    subsequences: a list of numpy vector
        each vector is one subsequence
        contains the index of periodic peaks

    '''

    assert_vector(peaksTime)
    assert_monotonic(peaksTime)

    subsIndex = relative_error_periodic_subsequence(peaksTime, eps, alpha, low, high, min_length, max_length)

    subsequences = []
    for s in subsIndex:
        tmp = [peaksIndex[i] for i in s]
        subsequences.append(np.array(tmp))

    return subsequences


def relative_error_periodic_subsequence(a, eps, alpha, low, high, min_length, max_length):
    '''
    Approximation algorithm that find eps-periodic subsequences
    '''

    assert_vector(a)
    assert_monotonic(a)

    subsequences = []

    n_steps = np.ceil(np.log(high / low) / np.log(1 + eps)).astype(int)
    for i in range(n_steps):
        pmin = low * np.power((1 + eps), i)
        pmax = pmin * (1 + eps) * (1+alpha)

        if pmax > high:
            break

        logger.info("pmin {:0.2f} and pmax {:0.2f}".format(pmin, pmax))

        seqs = absolute_error_periodic_subsequence(a, pmin, pmax)
        seqs = [np.array(s) for s in seqs if len(s) > min_length and len(s) < max_length]

        subsequences += seqs

    # sort subsequences by its start time
    start = [seq[0] for seq in subsequences]

    subsequences = [seq for _, seq in sorted(zip(start, subsequences), key=lambda pair:pair[0])]

    return subsequences


def absolute_error_periodic_subsequence(a, pmin, pmax):
    '''
    Return longest subsequences that is periodic
    Dynamic programming approach

    Parameters
    ----------

    a: list of increasing numbers

    '''

    assert_vector(a)
    assert_monotonic(a)

    N = len(a)

    traceback = {}
    for i in range(N):
        traceback[i] = []

    for i in range(1, N):
        valid = []
        for j in range(i - 1, -1, -1):
            if a[i] - a[j] > pmax:
                break
            if a[i] - a[j] >= pmin:
                valid.append(j)

        valid = list(reversed(valid))

        # now find valid predecessor for i
        for j in valid:
            if not traceback[j]:
                L = 2
            else:
                L = traceback[j][0]['L'] + 1

            predecessor = {'prev': j, 'L': L}

            tobe_kept = []
            for k in range(len(traceback[i])):
                if traceback[i][k]['L'] >= predecessor['L']:
                    tobe_kept.append(k)

            traceback[i] = [traceback[i][k] for k in tobe_kept]
            traceback[i].append(predecessor)

        # logger.debug(traceback[i])
    subsequences = []
    sequence = []
    i = N - 1

    while i >= 0:
        if traceback[i]:
            sequence.append(i)
            i = traceback[i][0]['prev']
        else:
            if len(sequence) > 0:
                sequence.append(i)
                reverse = list(reversed(sequence))
                subsequences.append(reverse)
                sequence = []
            i -= 1

    return list(reversed(subsequences))


def unittest():
    # peaksIndex = np.array([1,11,16,19,22,26,33,37,39,41,45,50,58,70,77,79,87,106,124,128,131,133,135,137,146,154,162,165,171,173,178,182,193,195,197,201,204,210,213,215,227,230,232,242,250,257,260,271,286,307,311,315,333,339,347,362,365,368,376,384,396,423,425,473,484,487,494,501,506,520,524,531,541,549,559,571,579,585,594,599,608])
    # peaksTime = np.array([1545945464660,1545945465160,1545945465410,1545945465560,1545945465710,1545945465910,1545945466260,1545945466460,1545945466560,1545945466660,1545945466860,1545945467110,1545945467510,1545945468110,1545945468460,1545945468560,1545945468960,1545945469910,1545945470810,1545945471010,1545945471160,1545945471260,1545945471360,1545945471460,1545945471910,1545945472310,1545945472710,1545945472860,1545945473160,1545945473260,1545945473510,1545945473710,1545945474260,1545945474360,1545945474460,1545945474660,1545945474810,1545945475110,1545945475260,1545945475360,1545945475960,1545945476110,1545945476210,1545945476710,1545945477110,1545945477460,1545945477610,1545945478160,1545945478910,1545945479960,1545945480160,1545945480360,1545945481260,1545945481560,1545945481960,1545945482710,1545945482860,1545945483010,1545945483410,1545945483810,1545945484410,1545945485760,1545945485860,1545945488260,1545945488810,1545945488960,1545945489310,1545945489660,1545945489910,1545945490610,1545945490810,1545945491160,1545945491660,1545945492060,1545945492560,1545945493160,1545945493560,1545945493860,1545945494310,1545945494560,1545945495010])
    
    peaksIndex = np.array([1,11,16,19,22,\
                            26,33,37,39,41,\
                            45,50,58,70,77,\
                            79,87,106,124,128])

    peaksTime = np.array([64660,65160,65410,65560,65710,\
                        65910,66260,66460,66560,66660,\
                        66860,67110,67510,68110,68460,\
                        68560,68960,69910,70810,71010])

    subsequences = periodic_subsequence(peaksIndex, peaksTime, min_length=4, max_length=100,
                                        eps=0.1, alpha=0.45, low=400, high=1200)
    print(subsequences)


def main():
    unittest()


if __name__ == '__main__':
    main()

