"""pytest unit tests for vibrationtesting"""

import numpy as np
import vibrationtesting as vt
import numpy.testing as nt

np.set_printoptions(precision=4, suppress=True)

M = np.array([[4, 0, 0],
              [0, 4, 0],
              [0, 0, 4]])
Cso = np.array([[.1, 0, 0],
                [0, 0, 0],
                [0, 0, 0]])
K = np.array([[8, -4, 0],
              [-4, 8, -4],
              [0, -4, 4]])
omega, zeta, Psi = vt.sos_modal(M, K)


#########################################################
# system.py tests
#########################################################

def test_d2c():
    Ad = np.array([[0.9999, 0.0001, 0.01, 0.],
                   [0., 0.9999, 0., 0.01],
                   [-0.014, 0.012, 0.9999, 0.0001],
                   [0.008, -0.014, 0.0001, 0.9999]])
    Bd = np.array([[0.],
                   [0.],
                   [0.],
                   [0.01]])
    C = np.array([[-1.4, 1.2, -0.0058, 0.0014]])
    D = np.array([[-0.2]])
    A, B, *_ = vt.d2c(Ad, Bd, C, D, 0.01)
    nt.assert_array_almost_equal(A,
                                 np.array([[-0.002999, 0.003999, 1.000053,
                                            -0.00006],
                                           [-0.004001, -0.002999,
                                            - 0.000023, 1.000053],
                                           [-1.400083, 1.200148,
                                            - 0.003, 0.003999],
                                           [0.800075, -1.400143, 0.006,
                                            -0.002999]]))

# def test_c2d():


# def test_ssfrf():


# def test_sos_frf():


# def test_so2ss():

# Damp- no test

def test_sos_modal():
    M = np.array([[4, 0, 0],
                  [0, 4, 0],
                  [0, 0, 4]])
    K = np.array([[8, -4, 0],
                  [-4, 8, -4],
                  [0, -4, 4]])
    omega, zeta, Psi = vt.sos_modal(M, K, K / 10)
    nt.assert_array_almost_equal(
        omega, np.array([0.445042,  1.24698,  1.801938]))
    K_diag = np.array([[0.198062,  0., -0.],
                       [0.,  1.554958, -0.],
                       [-0., -0.,  3.24698]])

    nt.assert_array_almost_equal(Psi.T@K@Psi, K_diag)

    K2 = K - np.eye(K.shape[0])@M * (Psi.T@K@Psi)[0, 0]
    omega, zeta, Psi = vt.sos_modal(M, K2)
    nt.assert_array_almost_equal(omega, np.array([0.,  1.164859,  1.746115]))
    Psi_true = np.array([[-0.163993,  0.368488, -0.295505],
                         [-0.295505,  0.163993,  0.368488],
                         [-0.368488, -0.295505, -0.163993]])
    nt.assert_array_almost_equal(Psi_true, Psi)

    # Diagonalizes?
    Psi_true = np.array([[0.,  0., -0.],
                         [-0.,  1.356896,  0.],
                         [-0.,  0.,  3.048917]])
    nt.assert_array_almost_equal(Psi.T@K2@Psi, Psi_true)

    # How about non-proportional damping

    C = K / 10
    C[0, 0] = 2 * C[0, 0]
    omega, zeta, Psi = vt.sos_modal(M, K2, C)

    #  Damping matrix cannot be completely diagonalized.

    nt.assert_array_almost_equal(omega, np.array([0.,  1.164859,  1.746115]))

    nt.assert_array_almost_equal(zeta, np.array([0.,  0.113371,  0.112981]))
    C_diag = np.array([[0.041321, -0.048343,  0.038768],
                       [-0.048343,  0.264123, -0.087112],
                       [0.038768, -0.087112,  0.394556]])
    nt.assert_array_almost_equal(C_diag, Psi.T@C@Psi)


def test_serep():
    M = np.array([[4, 0, 0],
                  [0, 4, 0],
                  [0, 0, 4]])
    K = np.array([[8, -4, 0],
                  [-4, 8, -4],
                  [0, -4, 4]])
    retained = np.array([[1, 2]])
    Mred, Kred, T, truncated_dofs = vt.serep(M, K, retained)
    Mr_soln = np.array([[16.98791841, -16.19566936],
                        [-16.19566936,  24.19566936]])
    Kr_soln = np.array([[20.98791841, -12.98791841],
                        [-12.98791841,  10.21983253]])
    nt.assert_array_almost_equal(Mred, Mr_soln)
    nt.assert_array_almost_equal(Kred, Kr_soln)


# def test_guyan():


# def test_mode_expansion_from_model():


# def improved_reduction(when written):


# def test_model_correction_direct():


# slice- no test


# def test_rsolve():


# def test_real_modes():


def test_ss_modal():
    Bt = np.array([[1], [0], [0]])
    Ca = np.array([[1, 0, 0]])
    Cd = Cv = np.zeros_like(Ca)
    A, B, C, D = vt.so2ss(M, Cso, K, Bt, Cd, Cv, Ca)
    Am, Bm, Cm, Dm, eigenvalues, modes = vt.ss_modal(A, B, C, D)
    nt.assert_array_almost_equal(Am, np.array(
        [[-0.0013 + 0.445j, 0.0000 + 0.j, 0.0000 + 0.j, 0.0000 + 0.j,
          0.0000 + 0.j, 0.0000 + 0.j],
         [0.0000 + 0.j, -0.0013 - 0.445j, 0.0000 + 0.j, 0.0000 + 0.j,
          0.0000 + 0.j, 0.0000 + 0.j],
            [0.0000 + 0.j, 0.0000 + 0.j, -0.0068 + 1.247j, 0.0000 + 0.j,
             0.0000 + 0.j, 0.0000 + 0.j],
            [0.0000 + 0.j, 0.0000 + 0.j, 0.0000 + 0.j, -0.0068 - 1.247j,
             0.0000 + 0.j, 0.0000 + 0.j],
            [0.0000 + 0.j, 0.0000 + 0.j, 0.0000 + 0.j, 0.0000 + 0.j,
             -0.0044 + 1.8019j, 0.0000 + 0.j],
            [0.0000 + 0.j, 0.0000 + 0.j, 0.0000 + 0.j, 0.0000 + 0.j,
             0.0000 + 0.j, -0.0044 - 1.8019j]]), decimal=3)
    nt.assert_array_almost_equal(Cm, np.array(
        [[0.0594 - 0.0001j, 0.0594 + 0.0001j, 0.0039 - 0.717j, 0.0039 + 0.717j,
          0.0241 - 0.9307j, 0.0241 + 0.9307j]]), decimal=3)


def test_sos_modal_non_rigid():
    omega, zeta, Psi = vt.sos_modal(M, K, K / 10)
    nt.assert_array_almost_equal(omega, np.array(
        [0.445,   1.247,   1.8019]), decimal=3)


def test_sos_modal_non_rigid_diag():
    omega, zeta, Psi = vt.sos_modal(M, K, K / 10)
    nt.assert_array_almost_equal(Psi.T@K@Psi,
                                 np.array([[0.1981,  0.,     -0.],
                                           [0.,      1.555,  -0.],
                                           [-0.,     -0.,      3.247]]),
                                 decimal=3)


def test_sos_modal_rigid():
    omega, zeta, Psi = vt.sos_modal(M, K)
    K2 = K - np.eye(K.shape[0])@M * (Psi.T@K@Psi)[0, 0]
    omega, zeta, Psi = vt.sos_modal(M, K2)
    nt.assert_array_almost_equal(omega, np.array(
        [0.,     1.1649, 1.7461]), decimal=3)


def test_sos_modal_rigid_diag():
    omega, zeta, Psi = vt.sos_modal(M, K)
    K2 = K - np.eye(K.shape[0])@M * (Psi.T@K@Psi)[0, 0]
    omega, zeta, Psi = vt.sos_modal(M, K2)
    nt.assert_array_almost_equal(Psi,
                                 np.array([[-0.164,   0.3685, -0.2955],
                                           [-0.2955,  0.164,   0.3685],
                                           [-0.3685, -0.2955, -0.164]]),
                                 decimal=3)


def test_sos_modal_non_proportional():
    omega, zeta, Psi = vt.sos_modal(M, K)
    K2 = K - np.eye(K.shape[0])@M * (Psi.T@K@Psi)[0, 0]
    C = K / 10
    C[0, 0] = 2 * C[0, 0]
    omega, zeta, Psi = vt.sos_modal(M, K2, C)
    nt.assert_array_almost_equal(omega,
                                 np.array([0.,     1.1649, 1.7461]), decimal=3)
    nt.assert_array_almost_equal(zeta,
                                 np.array([0.,     0.1134, 0.113]), decimal=3)
    nt.assert_array_almost_equal(Psi.T@C@Psi,
                                 np.array([[0.0413, -0.0483,  0.0388],
                                           [-0.0483,  0.2641, -0.0871],
                                           [0.0388, -0.0871,  0.3946]]),
                                 decimal=3)
