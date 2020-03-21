VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "ThisWorkbook"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Sub Stocks()
    
    Dim sheet As Worksheet

    For Each sheet In Worksheets

        sheet.Cells(1, 11).Value = "Ticker"
        sheet.Cells(1, 12).Value = "Yearly Change"
        sheet.Cells(1, 13).Value = "Percent Change"
        sheet.Cells(1, 14).Value = "Total Stock Volume"

        Dim ticker As String

        Dim year_open As Double
        year_open = 0

        Dim year_close As Double
        year_close = 0
        
        Dim yearly_change As Double
        yearly_change = 0

        Dim percent_change As Double
        percent_change = 0
        
        Dim total_stock_volume As Double
        total_stock_volume = 0
        
        Dim rowcount As Long
        rowcount = 2

        Dim lastrow As Long
        lastrow = sheet.Cells(Rows.Count, 1).End(xlUp).Row

        For i = 2 To lastrow
            
            If sheet.Cells(i, 1).Value <> sheet.Cells(i - 1, 1).Value Then

                year_open = sheet.Cells(i, 3).Value

            End If

            total_stock_volume = total_stock_volume + sheet.Cells(i, 7)

            If sheet.Cells(i, 1).Value <> sheet.Cells(i + 1, 1).Value Then

                sheet.Cells(rowcount, 11).Value = sheet.Cells(i, 1).Value

                sheet.Cells(rowcount, 14).Value = total_stock_volume

                year_close = sheet.Cells(i, 6).Value

                yearly_change = year_close - year_open
                sheet.Cells(rowcount, 12).Value = yearly_change

                If yearly_change >= 0 Then
                    sheet.Cells(rowcount, 12).Interior.ColorIndex = 4
                Else
                    sheet.Cells(rowcount, 12).Interior.ColorIndex = 3
                End If

                If year_open = 0 And year_close = 0 Then
                    percent_change = 0
                    sheet.Cells(rowcount, 13).Value = percent_change
                ElseIf year_open = 0 Then
                    sheet.Cells(rowcount, 13).Value = percent_change
                Else
                    percent_change = yearly_change / year_open
                    sheet.Cells(rowcount, 13).Value = percent_change
                    sheet.Cells(rowcount, 13).NumberFormat = "0.00%"
                End If

                rowcount = rowcount + 1
                
                year_open = 0
                year_close = 0
                yearly_change = 0
                percent_change = 0
                total_stock_volume = 0
                
            End If
        Next i

        sheet.Cells(2, 17).Value = "Greatest % Increase"
        sheet.Cells(3, 17).Value = "Greatest % Decrease"
        sheet.Cells(4, 17).Value = "Greatest Total Volume"
        sheet.Cells(1, 18).Value = "Ticker"
        sheet.Cells(1, 19).Value = "Value"

        lastrow = sheet.Cells(Rows.Count, 11).End(xlUp).Row

        Dim greatest_increase_stock As String
        Dim greatest_increase_value As Double

        greatest_increase_value = sheet.Cells(2, 13).Value

        Dim greatest_decrease_stock As String
        Dim greatest_decrease_value As Double

        greatest_decrease_value = sheet.Cells(2, 13).Value

        Dim greatest_total_volume_stock As String
        Dim greatest_total_volume_value As Double

        greatest_total_volume_value = sheet.Cells(2, 14).Value

        For j = 2 To lastrow

            If sheet.Cells(j, 13).Value > greatest_increase_value Then
                greatest_increase_value = sheet.Cells(j, 13).Value
                greatest_increase_stock = sheet.Cells(j, 11).Value
            End If

            If sheet.Cells(j, 13).Value < greatest_decrease_value Then
                greatest_decrease_value = sheet.Cells(j, 13).Value
                greatest_decrease_stock = sheet.Cells(j, 11).Value
            End If

            If sheet.Cells(j, 14).Value > greatest_total_volume_value Then
                greatest_total_volume_value = sheet.Cells(j, 14).Value
                greatest_total_volume_stock = sheet.Cells(j, 11).Value
            End If

        Next j

        sheet.Cells(2, 18).Value = greatest_increase_stock
        sheet.Cells(2, 19).Value = greatest_increase_value
        sheet.Cells(2, 19).NumberFormat = "0.00%"
        sheet.Cells(3, 18).Value = greatest_decrease_stock
        sheet.Cells(3, 19).Value = greatest_decrease_value
        sheet.Cells(3, 19).NumberFormat = "0.00%"
        sheet.Cells(4, 18).Value = greatest_total_volume_stock
        sheet.Cells(4, 19).Value = greatest_total_volume_value

    Next sheet

End Sub

