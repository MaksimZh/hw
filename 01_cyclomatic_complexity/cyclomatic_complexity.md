--------------------------------------------------------------------------------
1) Функция со сложными математическими расчётами
Вычисление величин ct и g (помечены )
--------------------------------------------------------------------------------
def _calcCoefs(mxL, lj, coefsNum, atol):
    mxSize = mxL[0].shape[0]
    factor = ArrayPoly([-lj, 1])
    dtype = np.common_type(mxL[0].coefs, factor.coefs)
    mxX, mxY, kappa = \
        _calcSmithN(mxL[0], num=coefsNum, factor=factor, atol=atol)
    alpha, beta = _calcAlphaBeta(kappa)
    mxXt = _calcXt(p=factor, x=mxX, kappa=kappa)
    mxLt = _calcLt(mxL=mxL, p=factor, beta=beta)
    kernelSize = sum(k > 0 for k in kappa[0])
    jordanChainsLen = kappa[0][-kernelSize:]
    del mxX, factor, kappa
    # TODO - move calculation of ct to separate function
    ct = []
    for k in range(kernelSize):
        ctk = np.zeros((coefsNum, alpha + jordanChainsLen[k], mxSize, 1),
            dtype=dtype)
        for n in range(coefsNum):
            nDeriv = beta[n] + jordanChainsLen[k]
            if n == 0:
                b = [_ort(mxSize, -1 - kernelSize + k + 1)]
            else:
                b = _calcB(mxY[n], mxLt[n], lj, ctk[:n, :nDeriv])
            ctk[n, :nDeriv] = _calcCt(mxXt[n], lj, b, nDeriv)
            del nDeriv, b
        ct.append(ctk)
        del ctk
    del mxY, mxXt, mxLt
    # TODO - move calculation of g to separate function
    g = []
    for k in range(kernelSize):
        gk = []
        for q in range(jordanChainsLen[k]):
            gkq = np.zeros((coefsNum, alpha + q + 1, mxSize, 1), dtype=complex)
            for n in range(coefsNum):
                num_ln_terms = beta[n] + q
                pow_deriv_coef = factorial(alpha + q) / factorial(num_ln_terms)
                for m in range(num_ln_terms + 1):
                    gkq[n, m] = pow_deriv_coef * ct[k][n, num_ln_terms - m]
                    pow_deriv_coef *= (num_ln_terms - m) / (m + 1)
                del num_ln_terms, pow_deriv_coef
            while gkq.shape[1] > 1 and np.max(np.abs(gkq[:, -1])) < atol:
                gkq = gkq[:, :-1]
            gk.append(gkq)
            del gkq
        g.append(gk)
        del gk
    return g
--------------------------------------------------------------------------------
Действия:
1)
--------------------------------------------------------------------------------
def _calcCoefs(mxL, lj, atol):
    ct = _calcAllCt(mxL, lj, atol)
    return [_calcG(ctk, atol) for ctk in ct]
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
