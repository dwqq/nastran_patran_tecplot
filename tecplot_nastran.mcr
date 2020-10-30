#!MC 1410
$!ReadDataSet  '"StandardSyntax" "1.0" "FEALoaderVersion" "443" "FILENAME_File" "E:\work\nastran_patran\code\nastran_bdf_test\nastran_test_0\test.op2" "SubdivideZonesBy" "Component" "AutoAssignStrandIDs" "Yes" "ZoneList" "5,3" "VarNameList" "Displacement" "InitialPlotType" "Cartesian3D" "ShowFirstZoneOnly" "No"'
  DataSetReader = 'MSC/NASTRAN Output2 (FEA)'
$!Pick AddAtPosition
  X = 3.23404255319
  Y = 3.98404255319
  ConsiderStyle = Yes
$!View FitSurfaces
  ConsiderBlanking = Yes
$!GlobalRGB RedChannelVar = 4
$!GlobalRGB GreenChannelVar = 4
$!GlobalRGB BlueChannelVar = 4
$!FieldLayers ShowContour = Yes
$!SetContourVar 
  Var = 6
  ContourGroup = 1
  LevelInitMode = ResetToNice
$!SetContourVar 
  Var = 6
  ContourGroup = 2
  LevelInitMode = ResetToNice
$!Pick AddAtPosition
  X = 4.24468085106
  Y = 5.39893617021
  ConsiderStyle = Yes
$!View FitSurfaces
  ConsiderBlanking = Yes
$!ThreeDAxis AxisMode = XYZDependent
$!ThreeDAxis DepXToZRatio = 0.00040000000000000002
$!Pick AddAtPosition
  X = 5.25531914894
  Y = 6.02659574468
  ConsiderStyle = Yes
$!View FitSurfaces
  ConsiderBlanking = Yes
$!ThreeDView 
  PSIAngle = 79.1489
  ThetaAngle = 147.234
  ViewerPosition
    {
    X = -51.10067713354947
    Y = 97.16423892336597
    Z = 0.007375951792795703
    }
  ViewWidth = 22.3213
$!ExportSetup ImageWidth = 846
$!ExportSetup ExportFName = 'E:/work/nastran_patran/code/nastran_bdf_test/nastran_test_0/order_4.png'
$!Export 
  ExportRegion = CurrentFrame
$!Quit
