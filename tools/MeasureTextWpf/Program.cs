using System.Globalization;
using System.Text.Json;
using System.Windows;
using System.Windows.Media;

public sealed record MeasureRequest(
    string FontFamily,
    double FontSize,
    string[] Texts,
    double LetterSpacing = 0.0
);

public sealed record MeasureResponse(double[] Widths);

public static class Program
{
    [STAThread]
    public static void Main()
    {
        string input = Console.In.ReadToEnd();
        MeasureRequest request = JsonSerializer.Deserialize<MeasureRequest>(input)
            ?? throw new InvalidOperationException("Invalid request JSON.");

        FontFamily fontFamily = new(request.FontFamily);
        Typeface typeface = new(
            fontFamily,
            FontStyles.Normal,
            FontWeights.Normal,
            FontStretches.Normal
        );
        CultureInfo culture = CultureInfo.GetCultureInfo("ja-JP");

        double[] widths = request.Texts
            .Select(text =>
            {
                FormattedText formatted = new(
                    text,
                    culture,
                    FlowDirection.LeftToRight,
                    typeface,
                    request.FontSize,
                    Brushes.Black,
                    1.0
                );
                double spacing = Math.Max(0, text.Length - 1) * request.LetterSpacing;
                return formatted.WidthIncludingTrailingWhitespace + spacing;
            })
            .ToArray();

        Console.WriteLine(JsonSerializer.Serialize(new MeasureResponse(widths)));
    }
}
