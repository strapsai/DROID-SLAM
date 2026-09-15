import torch


def segment_mean_fixed(x, ix, dim_size):
    """Mean of x[:, e] over the edges e whose segment index ix[e] == k, for
    k in 0..dim_size-1, in a FIXED order: the edges of each segment are
    gathered in their sorted order and summed by one reduction, so the
    result is bit-identical run to run (no atomics) and the cost is one
    read of x plus one gather per segment. torch_scatter.scatter_mean
    accumulates with atomics (order-dependent bits) and its deterministic
    fallback sorts the whole tensor per call (measured 50x slower at the
    update aggregator's shape, 126 MB). Segments without an edge are zero,
    as scatter_mean leaves them."""
    order = torch.argsort(ix, stable=True)
    counts = torch.bincount(ix, minlength=dim_size)
    starts = torch.cumsum(counts, 0) - counts
    out = x.new_zeros((x.shape[0], dim_size) + tuple(x.shape[2:]))
    counts_l, starts_l = counts.tolist(), starts.tolist()
    for k in range(dim_size):
        n = counts_l[k]
        if n == 0:
            continue
        sel = order[starts_l[k]:starts_l[k] + n]
        out[:, k] = x.index_select(1, sel).sum(dim=1) / n
    return out
