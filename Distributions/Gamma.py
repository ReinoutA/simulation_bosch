import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, gamma

def plot_normal_distribution(mean, std, xmin=0, xmax=4, num_points=1000):
    # Genereer punten om de kansdichtheidsfunctie te plotten
    x = np.linspace(xmin, xmax, num_points)
    
    # Bereken de kansdichtheidsfunctie voor elk punt
    y = norm.pdf(x, mean, std)
    
    # Plot de kansdichtheidsfunctie
    plt.plot(x, y, label='Normal distribution\n (mean={}, std={})'.format(mean, std))
    
    # Kleur de oppervlakte onder de kansdichtheidsfunctie in
    plt.fill_between(x, y, color='skyblue', alpha=0.5)
    
    # Voeg labels toe
    plt.title("Normal distribution deadline")
    plt.xlabel('Deadline (weeks)')
    plt.ylabel('Probability')
    
    # Voeg legenda toe
    plt.legend()
    
    # Toon de plot
    plt.show()

def plot_gamma_distribution(shape, scale, xmin=30, xmax=150, num_points=1000):
    # Genereer punten om de kansdichtheidsfunctie te plotten
    x = np.linspace(xmin, xmax, num_points)
    
    # Bereken de kansdichtheidsfunctie voor elk punt
    y = gamma.pdf(x, shape, scale=scale)
    
    # Plot de kansdichtheidsfunctie
    plt.plot(x, y, label='Gamma distribution (shape={}, scale={})'.format(shape, scale))
    
    # Kleur de oppervlakte onder de kansdichtheidsfunctie in
    plt.fill_between(x, y, color='skyblue', alpha=0.5)
    
    # Voeg labels toe
    plt.title("Gamma distribution transition time")
    plt.xlabel('Transition time (min)')
    plt.ylabel('Probability')
    
    # Voeg legenda toe
    plt.legend()
    
    # Toon de plot
    plt.show()

# Parameters voor de gamma verdeling
shape_param = 4  # Vormparameter (kan worden aangepast)
scale_param = 14  # Schaalparameter (kan worden aangepast)

# Plot de gamma verdeling
# plot_gamma_distribution(shape_param, scale_param)
plot_normal_distribution(2, 0.5)