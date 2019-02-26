# Experiment Details

## FAVAE (proposal model)

We describe the hyper parameters used for the results in 2D Reaching dataset, 2D Wavy Reaching dataset and Sprites dataset. We search the parameters beta and best C is shown in dictionary bellow.  In Sprites dataset, we add the pre-encoder and post-decoder for encoding and decoding of images at each time step. The pre-encoding and post-decoding architectures are the same as "encode_frames" and "decode_frames" in the code implementing the Disentangled-Sequential-Autoencoder [This code is available](https://github.com/yatindandi/Disentangled-Sequential-Autoencoder) with conv_dim=48. We search the parameters from beta = 0 to beta = 100 and the best parameter is beta = 20 with C = [20, 10, 5].

```python
import numpy as np

seach_beta_dict = {
	'2d_reaching_1000':np.arange(0.00, 5.02, 0.5),
    '2d_wavy_reaching_1000':np.insert(np.arange(0.00, 140.02, 20), 0, 1.0),
    '2d_reaching_100':np.arange(0.0, 1.402, 0.2),
    '2d_wavy_reaching_100':np.insert(np.arange(0.0, 14.02, 2), 0, 1.0)
}

c_dict = {
             ('2d_reaching_100', '-'):'0.00,0.00,0.00',
             ('2d_reaching_100', 'L'):'0.00,0.00,0.99',
             ('2d_wavy_reaching_100', '-'):'7.84,0.00,0.00',
             ('2d_wavy_reaching_100', 'L'):'5.61,0.25,4.08',
             ('2d_reaching_1000', '-'):'1.17,0.00,0.00',
             ('2d_reaching_1000', 'L'):'1.35,0.00,1.29',
             ('2d_wavy_reaching_1000', '-'):'18.60,0.00,0.00',
             ('2d_wavy_reaching_1000', 'L'):'16.37,3.72,4.10'
}
```

## FHVAE (baseline model)

For the FHVAE experiments, we used the code from the implementation at [here](https://github.com/wnhsu/FactorizedHierarchicalVAE).
We used the recurrent setting with LSTM encoders and a decoder with unit size=256 and batch size=80. The dimensions of latent variables z1 and z2 wrer 7 for each. We used Adam optimizer with learning rate=0.001. We applied goal-position factors (2 classes for 2D Reaching and 5 classes for 2D Wavy Reaching) as label inputs. We varied alpha from 1.0 to 30.0, and the best alpha was alpha=1.0 for both 2D Reaching and 2D Wavy Reaching.