# README

## Quickstart

### Installation

`pip install profile-exp-rescale`

### Example

```python
>>> from profile_exp_rescale import rescale
>>> rescale([0, 10, 2, 3, 5], target_sum=30, target_max_value=15)

array([ 0. , 15. ,  3. ,  4.5,  7.5])
```

## Herleitung

### Gegeben

- Fläche alt: $\displaystyle F_a = \sum_{t=1}^T{x_t}$ mit $x_t \in [0, m], 0 < F_a$

- Fläche neu (kleiner als Fläche alt): $F_n$ mit $0 < F_n < F_a$

### Gesucht

Funktion $f(x)$ mit

- A) erhalte Maxima: $f(m) = m$ mit $m := max(x)$

- B) reduziere Fläche: $\displaystyle F_n = \sum_{t=1}^T{f(x_t)}$

- C) erhalte 0: $f(0) = 0$

- D) erhalte Ordnung, also $f(x_i) > f(x_j) \Leftrightarrow x_i > x_j \Rightarrow \frac{df}{dx} > 0$

Das Problem ist nicht eindeutig formuliert, die Reduktion der Fläche kann verschiedenartig auf die einzelnen Punkte verteilt werden.

### Lösung

- Wähle $\alpha > 0$
- $g(x) := m\displaystyle\frac{e^{\alpha x}-1}{e^{\alpha m}-1}$
- $\beta := \displaystyle\frac{F_a - F_n}{F_a - \displaystyle\sum_{t=1}^T{g(x_t)}}$
- ist $\beta \notin (0,1] \Rightarrow \alpha$ zu klein gewählt
- **Interpretation**: je größer $\alpha$, desto mehr werden die großen Werte reduziert. Je kleiner $\alpha$, desto mehr müssen
  die kleinen Werte die gewünschte Flächenreduktion erzielen. Ab einer gewissen Grenze ist das unmöglich, die Werte fallen
  unter 0 und D) gilt nicht mehr.
- **Gleichung**: $f(x) = x - \beta \left(x - g(x)\right)$
- für jedes $g(x)$, dass A), C) und D) erfüllt, werden A-D für $f(x)$ erfüllt.
- Idealerweise wird durch Optimierung ein Wert für $\alpha$ gefunden, für den $\beta$ möglichst bei 1 liegt (möglichst nahe an reiner e-Funktion)

### Beweis

Zeige A,C,D für $\displaystyle g(x) = m\frac{e^{\alpha x}-1}{e^{\alpha m}-1}$

- A)

$$
    \displaystyle g(m) = \\
    m\frac{e^{\alpha m}-1}{e^{\alpha m}-1} = \\
    m\frac{1}{1} = \\
    m
$$

- C)

$$
    g(0) = \\
    m\displaystyle\frac{e^{\alpha 0}-1}{e^{\alpha m}-1} = \\
    m\displaystyle\frac{1-1}{e^{\alpha m}-1} = \\
    m \times 0 = \\
    m
$$

- D)

$$
    g'(x) =
    m\alpha\displaystyle\frac{e^{\alpha x}}{e^{\alpha m}-1} \alpha > 0 \Rightarrow \\
    e^{\alpha x} > 1, e^{\alpha m} > 1, m\alpha > 0, e^{\alpha m} - 1 > 0 \Rightarrow \\
    g'(x) = [>0]\displaystyle\frac{[>1]}{[>0]} \\
    g'(x) > 0
$$

Zeige A,B,C,D für $f(x) = x - \beta \left(x - g(x)\right)$, wenn A,C,D für $g(x)$ gezeigt wurde

- A)

$$
    f(m) = \\
    m - \beta \left(m - g(m)\right) = \\
    m - \beta \left(m - m\right)  = \\
    m - 0 = \\
    m
$$

- B)

$$
    F_n = \\
    \displaystyle\sum_{t=1}^T{f(x_t)} = \\
    \displaystyle\sum_{t=1}^T{\left(x_t - \beta \left(x_t - g(x_t)\right)\right)} = \\
    \displaystyle\sum_{t=1}^T{x_t} - \beta \left( \displaystyle\sum_{t=1}^T{x_t} - \displaystyle\sum_{t=1}^T{g(x_t)} \right) = \\
    F_a - \frac{F_a - F_n}{F_a - \displaystyle\sum_{t=1}^T{g(x_t)}}\left(F_a - \displaystyle\sum_{t=1}^T{g(x_t)}\right) = \\
    F_a - \left(F_a - F_n\right) = \\
    F_n
$$

- C)

$$
    f(0) = \\
    0 - \beta \left(0 - g(0)\right) = \\
    0 - \beta \left(0 - 0\right)  = \\
    0 - 0 = \\
    0
$$

- D)

$$
    f'(x) = 1 - \beta \left(1 - g'(x)\right) \\
    g'(x) > 0, \beta \in (0,1) \Rightarrow \\
    1 - g'(x) < 1 \Rightarrow \\
    \beta \left(1 - g'(x)\right) < 1 \Rightarrow \\
    1 - \beta \left(1 - g'(x)\right) > 0 \Rightarrow \\
    f'(x) > 0
$$

### Varianten

- Bei einer **Erhöhung** der Fläche muss $\alpha$ negativ sein, der Rest bleibt gleich und kann analog bewiesen werden
- Bei einer Änderung der Fläche und gleichzeitiger Änderung des Maximums auf einen gewünschten Zielwert kann das Problem in zwei Teile geteilt werden:

  - lineare Skalierung, damit die Daten das gewünschte Maximum erhalten (0 bleibt erhalten)
  - Skalierungsverfahren wie oben anwenden, um die Zielfläche zu erhalten.

- Mittels eines einfachen Optimierungsverfahren (z.B. Bisektion) kann versucht werden, ein $\alpha$ zu finden, bei dem ein $\beta$ von 1 entsteht und die Funktion möglichst ausgeglichen reskaliert

### Bemerkung

Es gibt offensichtlich Grenzen, in denen eine Reskalierung möglich ist. So kann bei n Werten offensichtlich nicht auf einen Wert skaliert werden, der größer oder gleich $n * max(X)$ liegt.
