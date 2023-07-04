import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import os

try:
    import seaborn as sns

    sns.set_theme(
        style="darkgrid"
    )  # style must be one of: white, dark, whitegrid, darkgrid, ticks
except ModuleNotFoundError:
    print(
        f"\n\n\t{'-' * 70}\n\tWARNING: It is recommended to install 'seaborn' to get nicer plots.\n\t{'-' * 70}\n\n"
    )


def make_path(_path):
    if not os.path.exists(_path):
        os.makedirs(_path)


def plot_pdfs(
    dists,
    labels,
    colors=None,
    interval_prob=0.99,
    target=None,
    tit="",
    xl="",
    yl="pdf",
    _path="",
    _name="pdf plot",
    _format=".png",
    dpi=300,
    sz=16,
    _show_values=True,
):
    """
    "dists" is a list of scipy.stats distributions
    "interval_prob" is the cumulative distribution (central) based on which the plot's interval is set.
    """
    from matplotlib import rc

    rc("text", usetex=True)
    rc("font", size=sz)
    rc("legend", fontsize=sz)
    rc("text.latex", preamble=r"\usepackage{cmbright}")
    _name = _name.replace("$", "")  # in case of latex formatted name
    if tit is None:
        tit = "PDF"
    tit = tit.replace("_", "\_")  # suitable for latex formatted title
    xl = xl.replace("_", "\_")  # suitable for latex formatted title
    yl = yl.replace("_", "\_")  # suitable for latex formatted title
    medians = []
    ms = []
    stds = []
    xxs = []
    x_min = 1e20
    x_max = -1e20
    for d in dists:
        medians.append(d.median())
        ms.append(d.mean())
        stds.append(d.std())
        xd0, xd1 = d.interval(interval_prob)
        xxs.append(np.linspace(xd0, xd1, 1000))
        x_min = min(x_min, xd0)
        x_max = max(x_max, xd1)
    from math import isnan

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter("%.1e"))
    ax.xaxis.set_major_formatter(mtick.FormatStrFormatter("%.2e"))
    max_pdf = 0.0
    max_std = 0.0
    if colors is None:
        plt_options = len(dists) * [{"color": "black"}]
    else:
        plt_options = [{"color": cl} for cl in colors]
    for d, dist in enumerate(dists):
        if isnan(stds[d]):
            print(
                "WARNING: No pdf-plot for a distribution with an infinite standard deviation !"
            )
        else:
            m_ = np.format_float_scientific(ms[d], unique=False, precision=2)
            median_ = np.format_float_scientific(medians[d], unique=False, precision=2)
            std_ = np.format_float_scientific(stds[d], unique=False, precision=2)
            pdf_ = dist.pdf(xxs[d])
            if _show_values:
                label_ = (
                    labels[d]
                    + r": $\begin{array}{rcl} \mbox{median} & \mbox{=} & "
                    + str(median_)
                    + " \\\\ \mbox{mean} & \mbox{=} & "
                    + str(m_)
                    + " \\\\ \mbox{std} & \mbox{=} & "
                    + str(std_)
                    + " \end{array} $"
                )
            else:
                label_ = labels[d]
            plt.plot(xxs[d], pdf_, label=label_, **plt_options[d])
            t_min = 1e20
            t_max = -1e20
            max_pdf = max(np.max(pdf_), max_pdf)
            max_std = max(stds[d], max_std)
    if target is not None:
        if type(target) == list or type(target) == np.ndarray:
            for i, t in enumerate(target):
                target_ = np.format_float_scientific(t, unique=False, precision=2)
                plt.bar(
                    x=t,
                    height=1.0 * max_pdf,
                    width=max_std * 0.02,
                    color=PltOptions["perfect"]["color"],
                )
                if _show_values:
                    plt.text(
                        t,
                        0.9 * i * max_pdf / (len(target) - 1),
                        f"target{i}=\n{target_}",
                        ha="center",
                        va="bottom",
                        fontsize=sz,
                    )
                else:
                    plt.text(
                        t,
                        0.9 * i * max_pdf / (len(target) - 1),
                        f"target{i}",
                        ha="center",
                        va="bottom",
                        fontsize=sz,
                    )
            t_min, t_max = min(target), max(target)
        else:
            target_ = np.format_float_scientific(target, unique=False, precision=2)
            plt.bar(
                x=target,
                height=1.0 * max_pdf,
                width=max_std * 0.03,
                color=PltOptions["perfect"]["color"],
            )
            if _show_values:
                plt.text(
                    target,
                    0,
                    f"target={target_}",
                    ha="center",
                    va="bottom",
                    fontsize=sz,
                )
            else:
                plt.text(target, 0, f"target", ha="center", va="bottom", fontsize=sz)
            t_min, t_max = target, target
    plt.xticks(np.linspace(min(x_min, t_min), max(x_max, t_max), 3), fontsize=sz)
    plt.yticks(np.linspace(0.0, max_pdf, 3), fontsize=sz)
    plt.title(tit, fontsize=sz)
    plt.xlabel(xl, fontsize=sz)
    plt.ylabel(yl, fontsize=sz)
    plt.legend(fontsize=int(sz * 0.7), loc="best")
    plt.tight_layout()
    plt.savefig(_path + _name + _format, bbox_inches="tight", dpi=dpi)
    plt.show(block=False)
    plt.rcParams["text.usetex"] = False


def gaussian_error_propagator(jac, stds=None, cov=None, rtol=1e-12, atol=1e-6):
    """
    If we have some random parameters (like 'p') as inputs to a function like 'f':
    jac:
        the jacobian (derivative) of 'f' at p_mean (means of 'p'); i.e.:
            jac = d [f(p_mean)] / d [p_mean] .
    stds (a vector):
        standard deviations of 'p'.
    cov (if not None):
        the covariance of 'p'. --> its diagonal is stds**2 .

    --> At least one of 'stds' and 'cov' must be given.

    Returns:
        the full covariance matrix of f(p) .

    NOTEs:
    - The mean values of p; i.e. p_mean, do not matter!
    - The tolerances are meant for:
        - checking if stds and cov are in agreement (if both are given).
        - checking 'cov' to be symmetric, which is a requirement for the validity of the formula used.
    """
    if (stds is None) and (cov is None):
        raise ValueError(f"At least one of stds or cov must be given.")
    else:  # At least one of stds and/or cov is given.
        if (stds is not None) and (
            cov is not None
        ):  # if both 'stds' 'cov' are given, we check them to agree.
            e = np.linalg.norm(cov - np.diag(stds**2)) / np.linalg.norm(stds)
            if e > rtol:
                raise ValueError(
                    f"The diagonal values of the 'cov' do not agree with the 'stds'."
                )
        if cov is None:  # no correlation among the inputs are considered.
            assert len(stds) == jac.shape[1]
            return (jac @ np.diag(stds**2)) @ jac.T
            # NOTE: the diagonal entries will form: (jac**2) @ (np.array(stds)**2)
            # , however, the return value above has non-diagonal terms as well.
        else:
            assert cov.shape[0] == cov.shape[1] == jac.shape[1]
            if not np.allclose(cov, cov.T, rtol=rtol, atol=atol):
                # covariance matrix must be symmetric for the following formula to be valid.
                _e = np.linalg.norm(cov - cov.T) / np.linalg.norm(cov)
                _msg = f"Covariance matrix must be symmetric (needed for Gaussian uncertainty propagation)."
                _msg += f" Relative error = np.linalg.norm(cov-cov.T) / np.linalg.norm(cov) = {_e:.2e} ."
                raise ValueError(_msg)
            else:
                return (jac @ cov) @ jac.T
