import numpy as np

class NacaFourDigitAirfoil():

    def __init__(self, m, p, t):
        """
        m - max camber in percent of chord (0 to 9)
        p - location of max camber in percent of chord (0 to 9)
        t - max thickness divided by chord length (0 to 99)
        """
        self.m = 0.01 * m
        self.p = 0.1 * p
        self.t = 0.01 * t

    def get_thickness(self, x:np.array):
        """
        x - horizontal position (0 to 1)
        """
        t = self.t
        a_0 = 0.2969
        a_1 = -0.126
        a_2 = -0.3516
        a_3 = 0.2843
        a_4 = -0.1015
        dyt_dt = 5 * (a_0*np.sqrt(x) + a_1*x + a_2*x**2 + a_3*x**3 + a_4*x**4)
        yt = t * dyt_dt
        return yt

    def get_camber(self, x:np.array):
        """
        x - horizontal position (0 to 1)
        """
        m = self.m
        p = self.p
        
        dum = x <= p
        dyc_dm = np.zeros(x.shape)
        if p > 0:
            dyc_dm[dum] = 1.0/(p**2) * (2*p*x[dum] - x[dum]**2)
        if p < 1:
            dyc_dm[~dum] = 1.0/((1-p)**2) * (1 - 2*p + 2*p*x[~dum] - x[~dum]**2)
        
        yc = m*dyc_dm
        
        return yc

    def get_camber_angle(self, x:np.array):
        m = self.m
        p = self.p
    
        dum = x <= p
        dyc_dx = np.zeros(x.shape)
        if p > 0:
            dyc_dx[dum] = 2.0*m/(p**2) * (p - x[dum])
        if p < 1:
            dyc_dx[~dum] = 2.0*m/((1-p)**2)*(p - x[~dum])
        return np.arctan(dyc_dx)

    def get_upper(self, x:np.array):
        yt = self.get_thickness(x)
        yc = self.get_camber(x)
        
        theta = self.get_camber_angle(x)
        xu = x - yt*np.sin(theta)
        yu = yc + yt*np.cos(theta)
        
        return xu, yu
        
    def get_lower(self, x:np.array):
        yt = self.get_thickness(x)
        yc = self.get_camber(x)

        theta = self.get_camber_angle(x)
        xl = x + yt*np.sin(theta)
        yl = yc - yt*np.cos(theta)
        
        return xl, yl
