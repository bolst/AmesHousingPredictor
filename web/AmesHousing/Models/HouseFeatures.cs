namespace AmesHousing.Models;

public record HouseFeatures
{

    public int MSSubClass { get; set; }

    public string MSZoning { get; set; }

    public double LotFrontage { get; set; }

    public int LotArea { get; set; }

    public string Street { get; set; }

    public string Alley { get; set; }

    public string LotShape { get; set; }

    public string LandContour { get; set; }

    public string Utilities { get; set; }

    public string LotConfig { get; set; }

    public string LandSlope { get; set; }

    public string Neighborhood { get; set; }

    public string Condition1 { get; set; }

    public string Condition2 { get; set; }

    public string BldgType { get; set; }

    public string HouseStyle { get; set; }

    public int OverallQual { get; set; }

    public int OverallCond { get; set; }

    public int YearBuilt { get; set; }

    public int YearRemodAdd { get; set; }

    public string RoofStyle { get; set; }

    public string RoofMatl { get; set; }

    public string Exterior1st { get; set; }

    public string Exterior2nd { get; set; }

    public string MasVnrType { get; set; }

    public double MasVnrArea { get; set; }

    public string ExterQual { get; set; }

    public string ExterCond { get; set; }

    public string Foundation { get; set; }

    public string BsmtQual { get; set; }

    public string BsmtCond { get; set; }

    public string BsmtExposure { get; set; }

    public string BsmtFinType1 { get; set; }

    public int BsmtFinSF1 { get; set; }

    public string BsmtFinType2 { get; set; }

    public int BsmtFinSF2 { get; set; }

    public int BsmtUnfSF { get; set; }

    public int TotalBsmtSF { get; set; }

    public string Heating { get; set; }

    public string HeatingQC { get; set; }

    public string CentralAir { get; set; }

    public string Electrical { get; set; }

    public int n1stFlrSF { get; set; }

    public int n2ndFlrSF { get; set; }

    public int LowQualFinSF { get; set; }

    public int GrLivArea { get; set; }

    public int BsmtFullBath { get; set; }

    public int BsmtHalfBath { get; set; }

    public int FullBath { get; set; }

    public int HalfBath { get; set; }

    public int BedroomAbvGr { get; set; }

    public int KitchenAbvGr { get; set; }

    public string KitchenQual { get; set; }

    public int TotRmsAbvGrd { get; set; }

    public string Functional { get; set; }

    public int Fireplaces { get; set; }

    public string FireplaceQu { get; set; }

    public string GarageType { get; set; }

    public double GarageYrBlt { get; set; }

    public string GarageFinish { get; set; }

    public int GarageCars { get; set; }

    public int GarageArea { get; set; }

    public string GarageQual { get; set; }

    public string GarageCond { get; set; }

    public string PavedDrive { get; set; }

    public int WoodDeckSF { get; set; }

    public int OpenPorchSF { get; set; }

    public int EnclosedPorch { get; set; }

    public int n3SsnPorch { get; set; }

    public int ScreenPorch { get; set; }

    public int PoolArea { get; set; }

    public string PoolQC { get; set; }

    public string Fence { get; set; }

    public string MiscFeature { get; set; }

    public int MiscVal { get; set; }

    public int MoSold { get; set; }

    public int YrSold { get; set; }

    public string SaleType { get; set; }

    public string SaleCondition { get; set; }

    public int? SalePrice { get; set; }

}
