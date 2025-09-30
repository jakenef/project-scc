import matplotlib.pyplot as plt

# Run scc.py to populate the runtimes
from _runtimes import runtimes


def main():
    # Define this
    def theoretical_big_o(v, e):
        return v+e

    # Fill in from result using compute_coefficient
    coeff = 3.9074507252752915e-07

    vv = [v for _, _, v, _, _ in runtimes]
    ee = [e for _, _, _, e, _ in runtimes]

    times = [t for _, _, _, _, t in runtimes]

    # Plot empirical values
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(vv, ee, times, marker='o')

    predicted_runtime = [
        coeff * theoretical_big_o(v, e)
        for d, s, v, e, t in runtimes
    ]

    # Plot theoretical fit
    ax.plot(
        vv,
        ee,
        predicted_runtime,
        c='k',
        ls=':',
        lw=2,
        alpha=0.5
    )

    # Update title, legend, and axis labels as needed
    ax.legend(['Observed', 'Theoretical O(v+e)'])
    ax.set_xlabel('|V|')
    ax.set_ylabel('|E|')
    ax.set_zlabel('Runtime')
    ax.set_title('Time for SCC on Graph')

    # You are welcome to play with the view angle as you'd like
    # elev=90 might be interesting
    ax.view_init(elev=10, azim=-60)

    fig.show()
    fig.savefig('_analysis/empirical.svg')


if __name__ == '__main__':
    main()
