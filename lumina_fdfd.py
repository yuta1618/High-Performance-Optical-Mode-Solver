import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import matplotlib.pyplot as plt

class Material:
    def __init__(self, n_real, n_imag=0.0):
        self.eps = (n_real + 1j * n_imag)**2

class Simulation:
    def __init__(self, window_size, resolution):
        self.Sx, self.Sy = window_size
        self.dx, self.dy = resolution
        self.Nx = int(np.ceil(self.Sx / self.dx))
        self.Ny = int(np.ceil(self.Sy / self.dy))
        self.dx, self.dy = self.Sx / self.Nx, self.Sy / self.Ny
        self.eps_r = np.ones((2 * self.Nx, 2 * self.Ny), dtype=complex)
        self.x = np.linspace(-self.Sx/2, self.Sx/2, self.Nx)
        self.y = np.linspace(-self.Sy/2, self.Sy/2, self.Ny)

    def add_rect(self, x0, y0, w, h, material):
        nx1, nx2 = self._to_idx(x0 - w/2, x0 + w/2, self.Sx, self.dx/2)
        ny1, ny2 = self._to_idx(y0 - h/2, y0 + h/2, self.Sy, self.dy/2)
        self.eps_r[nx1:nx2, ny1:ny2] = material.eps

    def _to_idx(self, v1, v2, size, res):
        idx1 = int(round((v1 + size/2) / res))
        idx2 = int(round((v2 + size/2) / res))
        return max(0, idx1), min(2*self.Nx, idx2)

    def _build_operators(self, k0):
        def diff_mat(N, delta, direction):
            d_f = sp.diags([-1, 1], [0, 1], shape=(N, N)).tolil()
            d_f[N-1, N-1] = -1
            d_b = sp.diags([-1, 1], [-1, 0], shape=(N, N)).tolil()
            d_b[0, 0] = 1
            if direction == 'x':
                return sp.kron(sp.eye(self.Ny), d_f.tocsc()) / (k0 * delta), \
                       sp.kron(sp.eye(self.Ny), d_b.tocsc()) / (k0 * delta)
            else:
                return sp.kron(d_f.tocsc(), sp.eye(self.Nx)) / (k0 * delta), \
                       sp.kron(d_b.tocsc(), sp.eye(self.Nx)) / (k0 * delta)

        DEX, DHX = diff_mat(self.Nx, self.dx, 'x')
        DEY, DHY = diff_mat(self.Ny, self.dy, 'y')
        return DEX, DEY, DHX, DHY

    def solve(self, wavelength, n_modes=1):
        k0 = 2.0 * np.pi / wavelength
        M = self.Nx * self.Ny
        er_xx = sp.diags(self.eps_r[1::2, 0::2].flatten(order='F'))
        er_yy = sp.diags(self.eps_r[0::2, 1::2].flatten(order='F'))
        er_zz_inv = sp.diags(1.0 / self.eps_r[0::2, 0::2].flatten(order='F'))
        DEX, DEY, DHX, DHY = self._build_operators(k0)

        P = sp.bmat([
            [DEX @ er_zz_inv @ DHY, -(DEX @ er_zz_inv @ DHX + sp.eye(M))],
            [DEY @ er_zz_inv @ DHY + sp.eye(M), -DEY @ er_zz_inv @ DHX]
        ], format="csc")
        Q = sp.bmat([
            [DHX @ DEY, -(DHX @ DEX + er_yy)],
            [DHY @ DEY + er_xx, -DHY @ DEX]
        ], format="csc")

        target_neff = np.sqrt(np.max(self.eps_r).real)
        vals, vecs = spla.eigs(P @ Q, k=n_modes, sigma=-(target_neff**2))
        return [Mode(np.sqrt(-vals[i]), vecs[:, i], self.Nx, self.Ny, self.x, self.y) for i in range(n_modes)]

class Mode:
    def __init__(self, neff, vec, Nx, Ny, x, y):
        self.neff, self.x, self.y = neff, x, y
        self.Ex = vec[:Nx*Ny].reshape((Nx, Ny), order='F')
        self.Ey = vec[Nx*Ny:].reshape((Nx, Ny), order='F')

    def plot(self):
        plt.figure(figsize=(7, 5))
        plt.pcolormesh(self.x, self.y, np.abs(self.Ex).T, cmap='magma', shading='auto')
        plt.title(f"Mode (n_eff = {self.neff.real:.4f})")
        plt.colorbar(); plt.show()