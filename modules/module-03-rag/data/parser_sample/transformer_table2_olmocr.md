Table 2: The Transformer achieves better BLEU scores than previous state-of-the-art models on the English-to-German and English-to-French newstest2014 tests at a fraction of the training cost.

<table>
  <tr>
    <th rowspan="2">Model</th>
    <th colspan="2">BLEU</th>
    <th colspan="2">Training Cost (FLOPs)</th>
  </tr>
  <tr>
    <th>EN-DE</th>
    <th>EN-FR</th>
    <th>EN-DE</th>
    <th>EN-FR</th>
  </tr>
  <tr>
    <td>ByteNet [18]</td>
    <td>23.75</td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>Deep-Att + PosUnk [39]</td>
    <td></td>
    <td>39.2</td>
    <td></td>
    <td>1.0 \cdot 10^{20}</td>
  </tr>
  <tr>
    <td>GNMT + RL [38]</td>
    <td>24.6</td>
    <td>39.92</td>
    <td>2.3 \cdot 10^{19}</td>
    <td>1.4 \cdot 10^{20}</td>
  </tr>
  <tr>
    <td>ConvS2S [9]</td>
    <td>25.16</td>
    <td>40.46</td>
    <td>9.6 \cdot 10^{18}</td>
    <td>1.5 \cdot 10^{20}</td>
  </tr>
  <tr>
    <td>MoE [32]</td>
    <td>26.03</td>
    <td>40.56</td>
    <td>2.0 \cdot 10^{19}</td>
    <td>1.2 \cdot 10^{20}</td>
  </tr>
  <tr>
    <td>Deep-Att + PosUnk Ensemble [39]</td>
    <td></td>
    <td>40.4</td>
    <td></td>
    <td>8.0 \cdot 10^{20}</td>
  </tr>
  <tr>
    <td>GNMT + RL Ensemble [38]</td>
    <td>26.30</td>
    <td>41.16</td>
    <td>1.8 \cdot 10^{20}</td>
    <td>1.1 \cdot 10^{21}</td>
  </tr>
  <tr>
    <td>ConvS2S Ensemble [9]</td>
    <td>26.36</td>
    <td><b>41.29</b></td>
    <td>7.7 \cdot 10^{19}</td>
    <td>1.2 \cdot 10^{21}</td>
  </tr>
  <tr>
    <td>Transformer (base model)</td>
    <td>27.3</td>
    <td>38.1</td>
    <td></td>
    <td><b>3.3 \cdot 10^{18}</b></td>
  </tr>
  <tr>
    <td>Transformer (big)</td>
    <td><b>28.4</b></td>
    <td><b>41.8</b></td>
    <td></td>
    <td>2.3 \cdot 10^{19}</td>
  </tr>
</table>
