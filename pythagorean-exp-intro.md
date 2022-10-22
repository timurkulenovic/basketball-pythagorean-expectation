## What is Pythagorean expectation?

Pythagorean expectation is a formula that was originally derived by Bill James to be used in baseball. The objective of the formula was to estimate how many wins a team should have won based on the number of runs scored and runs allowed. You can read more about the theorem on [Wikipedia](https://en.wikipedia.org/wiki/Pythagorean_expectation) and [this article](https://towardsdatascience.com/pythagorean-expectation-in-sports-analytics-with-examples-from-different-sports-f5e599530a6c) that also presents few practical examples. Originally the form of the formula looks like this:
$$
W \approx \frac{(\text{runs scored}) ^ 2}{(\text{runs scored}) ^ 2 + (\text{runs allowed}) ^ 2} \text{,}
$$
where $W$ is the ratio of team's wins or **win percentage**.

However, we can generalize the above formula to other sports. If we use general notation, where $P_F$ denotes *points for* and $P_A$ denotes *points against*, then formula then converts to:

$$
W \approx \frac{{P_F} ^ x}{P_F ^ x + P_A ^ x} \text{.}
$$

Notice that in the second formula the exponents undefined. As seen in the first formula for baseball, Bill James used $x = 2$. Later there were some corrections for baseball to set $x = 1.83$. The value of $x$ depends on the nature of the sport, in football for example we see way lower number of points (goals) scored in comparison to basketball, so in order for the formula to be a good estimator of win percentage we need to set the $x$ value correctly.

## Example on Euroleague

In this article I will demonstrate how well does Pythagorean theorem apply to basketball, specifically to the strongest european competition of Turkish Airlines Euroleague.

For the analysis I used seasons of 2016/2017, 2017/2018, 2018/2019 and 2020/2021.

Let's first draw a plot of Pythagorean expectation (Pyth. exp.) vs. winning ratio for each team in listed seasons. Here, I used $x = 2$ just to show that we can also draw conclusions with *original* exponent.


    
![png](pythagorean-exp-intro_files/pythagorean-exp-intro_9_0.png)
    


We observe that the values on vertical and horizontal axis are not in the same range, therefore we conclude that the $x = 2$ is not the best setting for this data. However, there definitely is a linear relationship between winning ratio and Pythagorean expectation. Green line in plots presents the line obtained by linear regression. Additionally, I also calculated Pearson correlation coefficients are also calculated to confirm the linear relationship:




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>season</th>
      <th>corr</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2016/17</td>
      <td>0.954</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2017/18</td>
      <td>0.887</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2018/19</td>
      <td>0.963</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2020/21</td>
      <td>0.945</td>
    </tr>
  </tbody>
</table>
</div>



### Finding the best exponent

We observe that there is obvious correlation between Pythagorean expectation and winning ratio, however $x = 2$ is not the choice to directly estimate winning ratio from points. To get the best fit for $x$ I constructed simple loss function:
$$
L(x) = \frac{\sum_{i=1}^n | W_i - \frac{{P_{F_i}} ^ x}{P_{F_i} ^ x + P_{A_i} ^ x}|}{n} \text{.}
$$
The loss function minimizes the average difference between winning ratio and Pythagorean expectation across all teams with respect to parameter $x$. For loss function minimization I used function `fmin_l_bfgs_b` from `scipy` library. The values were calculated for each season separately:






<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Season</th>
      <th>Best x</th>
      <th>error</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2016/17</td>
      <td>11.24</td>
      <td>0.034</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2017/18</td>
      <td>10.95</td>
      <td>0.056</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2018/19</td>
      <td>11.03</td>
      <td>0.039</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2020/21</td>
      <td>11.10</td>
      <td>0.041</td>
    </tr>
  </tbody>
</table>
</div>



The best fits for each of four seasons are pretty similar, $x \approx 11$. It could be that the $L(x)$ has multiple local minima and `fmin_l_bfgs_b` might not have returned the global minimum. We can verify that these $x$ values are indeed the best fit with respect to $L(x)$ using brute force by simply evaluating function from on range [0, 30] with step of 0.05.


    
![png](pythagorean-exp-intro_files/pythagorean-exp-intro_17_0.png)
    


These seem to be convex functions, so there should not be any problems getting the smallest error using any of two methods. Quick glance at Loss vs. x plots suffices to confirm that $x \approx 11$ seems to be a good fit for this data, however we also can also show values obtained using this method:




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Season</th>
      <th>Best x</th>
      <th>Error</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2016/17</td>
      <td>11.25</td>
      <td>0.034</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2017/18</td>
      <td>10.95</td>
      <td>0.056</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2018/19</td>
      <td>11.00</td>
      <td>0.039</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2020/21</td>
      <td>11.10</td>
      <td>0.041</td>
    </tr>
  </tbody>
</table>
</div>



Comparing both tables, we conclude that the values are more or less identical.

### Pythagorean expectation using best exponent

Finally, we use the obtained values for $x$ to fix the Pythagorean expectation to get the best fit to given data. Note that green line in this case, does not represent the line obtained linear regression, it is simply just $y = x$ line.







    
![png](pythagorean-exp-intro_files/pythagorean-exp-intro_23_0.png)
    


Again, we confirm strong linear correlation between Pythagorean expectation and winning ratio:




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>season</th>
      <th>corr</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2016/17</td>
      <td>0.956</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2017/18</td>
      <td>0.884</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2018/19</td>
      <td>0.967</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2020/21</td>
      <td>0.944</td>
    </tr>
  </tbody>
</table>
</div>



Here, the interpretation of the plots should the following: the teams that are above the line managed to win fewer games than expected, considering the number of points scored and allowed. The teams that are below the line managed to win more games than expected.

Few examples:
<ul>
    <li>In 2017/2018 Barcelona finished 13th, however they definitely had potential to reach the Top 8</li>
    <li>In 2020/2021 Fenerbahce finished 7th with winning ratio close to 0.6, but it seems that they had some luck on their side, since their expected winning ratio is below 0.5, which would leave them without Top 8.</li>
</ul>
