namespace AmesHousing.Api;

public record GetPricedHousesResponse
{
    public List<AmesHouse> Houses { get; set; }
    public int Page { get; set; }
    public int PageSize { get; set; }
    public int TotalItems { get; set; }
}