import os
import pandas as pd


def main(filepath):
    df = pd.read_csv(filepath)
    columns = [(col, df[col].dtype.name) for col in df.columns if col not in ['Id']]

    # types = [t.name for t in df.dtypes.unique()]

    pyCSharpType = {
        'int64': 'int',
        'object': 'string',
        'float64': 'double'
    }

    allClassesStr = '''namespace AmesHousing.Api;

public record AmesHouse
{
    '''

    for column, ctype in columns:
        cSharpType = pyCSharpType[ctype]

        if column[0].isdigit():
            column = 'n' + column

        if column == 'SalePrice':
            cSharpType += '?' # SalePrice can be null

        if cSharpType:
            allClassesStr += f'''
    public {cSharpType} {column} {{ get; set; }}
    '''

    allClassesStr += '\n}'

    print('done. output:')
    print(allClassesStr)

    os.makedirs(basePath := '../AmesHousing/Api/Models', exist_ok=True)

    with open(f'{basePath}/AmesHouse.cs', 'w+') as outfile:
        outfile.write(allClassesStr)



if __name__ == '__main__':
    train = '../../data/house-prices-advanced-regression-techniques/train.csv'
    main(train)
