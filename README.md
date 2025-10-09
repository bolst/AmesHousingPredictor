# Ames Housing Predictor

## Using notebooks

1. Download the dataset from the [Kaggle Repo](https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques/overview)
2. Place extracted folder into `data` folder. Structure should look like:

```bash
.
├── data
│   └── house-prices-advanced-regression-techniques
│       ├── data_description.txt
│       ├── test.csv
│       └── train.csv
├── notebooks
│   └── ...
├── ...
```

3. Create a virtual environment and activate (most IDEs can do this for you)

```bash
>> python3 -m venv venv
>> source venv/bin/activate
```

4. Add required libraries

```bash
>> pip3 install --upgrade pip
>> pip3 install -r requirements.txt
```

5. Start the Jupyter server (most IDEs will do this for you)

```bash
>> jupyter lab
```