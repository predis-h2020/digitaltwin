import sys
if './examples/VB_ASR/' not in sys.path:
    sys.path.append('./examples/VB_ASR/')

from helpers import *
from bayem import vba, MVN, Gamma

eps_0 = 0.
X0 = [0.1825, 38.21, 167.9]
return_jacobian = True
_path = f"./examples/VB_ASR/results/"
make_path(_path)

###############################
    # DATA
###############################

# ts_data = np.array([0, 8, 14, 19, 26, 46, 84, 123, 140, 173, 197, 200, 235, 252, 264, 284, 322, 361])
# epss_data = [0, 0.01, 0.01, 0, 0, 0.01, 0.02, 0.01, 0.04, 0.08, 0.09, 0.09, 0.11, 0.13, 0.12, 0.13, 0.14, 0.13]

ts_data = np.array([0, 8, 14, 19, 26, 46, 84, 123, 140, 173, 197, 200, 235, 252, 264, 284, 322, 361])
epss_data = [0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.027, 0.059, 0.092, 0.126, 0.143, 0.155, 0.161, 0.172, 0.182, 0.185]

###############################
    # MODEL
###############################

def eps_total(t, eps_inf=X0[0], Tau_c=X0[1], Tau_L=X0[2]):
    if return_jacobian:
        z, dz = zeta_func(t, Tau_c, Tau_L)
        diffs = [z, eps_inf * dz[0], eps_inf * dz[1]]
        return eps_0 + eps_inf * z, np.array(diffs).T
    else:
        z = zeta_func(t, Tau_c, Tau_L)
        return eps_0 + eps_inf * z
    
def zeta_func(t, Tau_c, Tau_L):
    a1 = np.exp(- t / Tau_c)
    a2 = np.exp((-t + Tau_L) / Tau_c)
    if return_jacobian:
        d1 = - t * a1 / (Tau_c**2*(a2 + 1.))
        d1 += (1. - a1) * (-t + Tau_L) * a2 / (Tau_c**2 * (a2 + 1.)**2)
        d2 = - (1. - a1) * a2 / (Tau_c * ( a2 + 1.)**2)
        return (1. - a1) / (1. + a2), np.array([d1, d2])
    else:
        return (1. - a1) / (1. + a2)

###############################
    # OBJECTIVE (MODEL ERROR)
###############################

def me_vec(X):
    eps_inf, Tau_c, Tau_L = X
    if return_jacobian:
        f, diff = eps_total(ts_data, eps_inf=eps_inf, Tau_c=Tau_c, Tau_L=Tau_L)
        return np.array(f) - np.array(epss_data), diff
    else:
        f = eps_total(ts_data, eps_inf=eps_inf, Tau_c=Tau_c, Tau_L=Tau_L)
        return np.array(f) - np.array(epss_data)

def me_scalar(X):
    if return_jacobian:
        f, diff = me_vec(X)
        return 0.5 * np.dot(f, f), f @ diff
    else:
        f = me_vec(X)
        return 0.5 * np.dot(f, f)

###############################
    # VARIATIONAL BAYESIAN (VB)
###############################

prior_mvn = MVN(mean=X0, precision=np.diag([(abs(x))**(-2) for x in X0]))
n0 = Gamma(shape=1.5, scale=175000.)
# n0 = Gamma(shape=0.84, scale=15000.)
# n0 = Gamma(shape=0.5, scale=500000.)
# n0 = Gamma(shape=0.84, scale=370000.)
vb_results = vba(f=me_vec, x0=prior_mvn, noise0=n0, jac=return_jacobian)

### Plot free energy
plt.figure()
n_vb = len(vb_results.free_energies)
xs = list(range(1, n_vb+1))
plt.plot(xs, vb_results.free_energies, marker='.')
plt.title(f"Free energy", size=12)
plt.xlabel('VB iteration', size=12)
plt.ylabel('F', size=12)
plt.xticks(xs)
plt.savefig(f"{_path}Free_energies.png", bbox_inches='tight', dpi=300)
plt.show()

### Plot Parameters
from scipy.stats import norm, gamma
pars_names = ['eps_inf', 'Tau_c', 'Tau_L']
pr_m = vb_results.param0.mean
pr_std = vb_results.param0.std_diag
post_m = vb_results.param.mean
post_std = vb_results.param.std_diag
noise0 = vb_results.noise0
options_prior = {'linestyle':'', 'color':'orange', 'marker':'<', 'fillstyle':'full'}
options_posterior = {'linestyle':'', 'color':'mediumblue', 'marker':'>', 'fillstyle':'full'}
options_predict = {'linestyle':'', 'color':'purple', 'marker':'d', 'fillstyle':'full'}
for i, n in enumerate(pars_names):
        pr_dist = norm(pr_m[i], pr_std[i])
        post_dist = norm(post_m[i], post_std[i])
        ## plot prior-posterior together
        plot_pdfs([pr_dist, post_dist], labels=['Prior', 'Posterior'], colors=[options_prior['color'] \
                , options_posterior['color']], tit=f"Parameter {n}" \
                  , xl=n, _path=_path, _name=f"Parameter_{n}", _format='.png', dpi=300, sz=16)

### Plot noises
interval_prob = 0.99
n0 = vb_results.noise0
sh_pr = n0.shape
sc_pr = n0.scale
n1 = vb_results.noise
sh_post = n1.shape
sc_post = n1.scale
g_pr = gamma(a=sh_pr, scale=sc_pr)
g_post = gamma(a=sh_post, scale=sc_post)
plot_pdfs([g_pr, g_post], labels=['Prior', 'Posterior'], colors=[options_prior['color'] \
        , options_posterior['color']], interval_prob=interval_prob \
            , tit=f"Inference of precision of noise", xl="$\phi$", _path=_path \
                , _name=f"Noise_precision", _format='.png', dpi=300, sz=16)


if return_jacobian:
    # propagation of parameters distributions into the model
    f_at_posterior, diff = eps_total(ts_data, eps_inf=post_m[0], Tau_c=post_m[1], Tau_L=post_m[2])
    cov = vb_results.param.cov
    cov_propagated = gaussian_error_propagator(jac=diff, stds=post_std \
                                                , cov=cov, rtol=1e-12, atol=1e-5)
    # uncertainty of the identified noise
    cov_inv = vb_results.cov_inv[0]
    cov_at_noise_mean = 1. / vb_results.noise.mean * np.linalg.inv(cov_inv)
    # Sum
    predicted_std_at_post = np.diag(cov_propagated + cov_at_noise_mean) ** (0.5)
else:
    f_at_posterior = eps_total(ts_data, eps_inf=post_m[0], Tau_c=post_m[1], Tau_L=post_m[2])
    print(f"Propagation of parameter variability into the model is ignored, since no jacobian is provided.")

###############################
    # SCIPY OPTIMIZE
###############################

import scipy.optimize as opt
method = 'trust-constr'
opt_results = opt.minimize(me_scalar, x0=X0, method=method, jac=return_jacobian)
print(opt_results)

###############################
    # PLOT ALL RESULTs
###############################

if return_jacobian:
    epss_0 = eps_total(ts_data)[0]
    epss_opt = eps_total(ts_data, *opt_results.x)[0]
else:
    epss_0 = eps_total(ts_data)
    epss_opt = eps_total(ts_data, *opt_results.x)
plt.figure()
plt.plot(ts_data, epss_data, linestyle='', marker='*', label='data', color='red')
plt.plot(ts_data, epss_0, linestyle='--', marker='.', label='model\n(initial guess)', color='gray')
plt.plot(ts_data, epss_opt, linestyle='--', marker='.', label='model\n(scipy-optimized)', color='green')
plt.plot(ts_data, f_at_posterior, linestyle='--', marker='o', fillstyle='none', label='model (mean)\n(VB-optimized)', color=options_predict['color'])
plt.fill_between(ts_data, f_at_posterior-2*predicted_std_at_post, f_at_posterior+2*predicted_std_at_post \
                          , label='model (4$\sigma$)\n(VB-optimized)', alpha=0.10, **{'color':options_predict['color']})
plt.xlabel('Time')
plt.ylabel('Expansion')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig(f"{_path}fitted_model_lab_scale.png", bbox_inches='tight', dpi=400)
plt.show()
