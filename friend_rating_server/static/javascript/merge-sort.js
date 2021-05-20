function mergeSort(arr, cmp, reverse=false) {
    let result = [];
    for (let i = 0; i < arr.length; i += 1) {
      result.push(undefined);
    }
    function mergeSortDomain(from, to) {
        if (from === to) {
            return;
        }
        let mid = Math.floor((from + to) / 2);
        mergeSortDomain(from, mid);
        mergeSortDomain(mid + 1, to);
        let i = from, j = mid + 1, k = from;
        while (i <= mid || j <= to) {
            if (i <= mid && j <= to) {
                if ((!reverse && cmp(arr[i], arr[j]) <= 0) || (reverse && cmp(arr[i], arr[j]) >= 0)) {
                    result[k] = arr[i];
                    i += 1;
                } else {
                    result[k] = arr[j];
                    j += 1;
                }
            } else if (i <= mid) {
                result[k] = arr[i];
                i += 1;
            } else {
                result[k] = arr[j];
                j += 1;
            }
            k += 1;
        }
        for (let l = from; l <= to; l += 1) {
            arr[l] = result[l];
        }
    }
    mergeSortDomain(0, arr.length - 1);
    return result;
}
