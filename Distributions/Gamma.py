import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gamma

def plot_gamma_distribution(shape, scale, xmin=30, xmax=150, num_points=1000):
    # Genereer punten om de kansdichtheidsfunctie te plotten
    x = np.linspace(xmin, xmax, num_points)
    
    # Bereken de kansdichtheidsfunctie voor elk punt
    y = gamma.pdf(x, shape, scale=scale)
    
    # Plot de kansdichtheidsfunctie
    plt.plot(x, y, label='Gamma Distributie (shape={}, scale={})'.format(shape, scale))
    
    # Kleur de oppervlakte onder de kansdichtheidsfunctie in
    plt.fill_between(x, y, color='skyblue', alpha=0.5)
    
    # Voeg labels toe
    plt.xlabel('Tijd (minuten)')
    plt.ylabel('Kansdichtheid')
    
    # Voeg legenda toe
    plt.legend()
    
    # Toon de plot
    plt.show()

# Parameters voor de gamma verdeling
shape_param = 4  # Vormparameter (kan worden aangepast)
scale_param = 10  # Schaalparameter (kan worden aangepast)

# Plot de gamma verdeling
plot_gamma_distribution(shape_param, scale_param)
