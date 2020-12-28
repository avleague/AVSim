module Pages where

import UIElem
import qualified Graphics.UI.Threepenny as UI
import Graphics.UI.Threepenny.Core
import System.Directory 

{-
Arquivo contém definições de html e css dos elementos da GUI
-}

folderPath,mapsPath,codesPath :: [Char]
--absoluteFolderPath = "C:/Users/GilmarCorreia/Desktop/2020-qs-paradigmas-diurno-projetofinal-GilmarCorreia/AVSim/simulator/"
folderPath = ".\\simulator\\"
mapsPath = folderPath ++ "UnrealEnvironments\\"
codesPath = folderPath ++ "Teams\\"

listOfMaps, listOfCodes :: IO [FilePath]
listOfMaps = getDirectoryContents mapsPath
listOfCodes = getDirectoryContents codesPath

leftPage :: UI Element
leftPage = UI.div # set UI.id_ "first"
                  # set UI.style [("background-color","#1f1f1f"),
                                  ("width", "50%"),
                                  ("height", "100%"),
                                  ("min-width", "10px")]
                  #+ elements
  where
    elements :: [UI Element]
    elements = do
      let mainTitle = UI.h1 # set text "AUTONOMOUS VEHICLE \n SIMULATOR"
                            # set UI.style [("text-align","center"),
                                            ("color"     ,"#ffcc00"),
                                            ("font-size" ,"50px"  ),
                                            ("font-weight", "bold"),
                                            ("font-family","Verdana"),
                                            ("margin-top","50px")]
                                      
          secondTitle = UI.h2 # set text "Select the Map to Launch"
                              # set UI.style [("text-align","center"),
                                              ("color"     ,"white"   ),
                                              ("font-size" ,"30px"  ),
                                              ("font-weight", "bold"),
                                              ("font-style", "italic"),
                                              ("margin-top","60px")]

          cbSelectMap = createComboBox "cbSelectMap" listOfMaps
          btnLaunchMap = createButton ("LAUNCH","btnLaunchMap")

          thirdTitle = UI.h2 # set text "Select the Code to Launch"
                              # set UI.style [("text-align","center"),
                                              ("color"     ,"white"   ),
                                              ("font-size" ,"30px"  ),
                                              ("font-weight", "bold"),
                                              ("font-style", "italic"),
                                              ("margin-top","30px")]

          cbSelectCode = createComboBox "cbSelectCode" listOfCodes

          btnExecAlg = createButton ("EXECUTE", "btnExecAlg")

          manual = UI.div # set UI.id_ "divManual"
                          # set UI.style [("position","relative"),
                                          ("margin","auto"),
                                          ("margin-top","70px"),
                                          ("display","block"),
                                          ("align-items", "center"),
                                          ("width","100%"),
                                          ("text-align","center")]
                          #+ [checkBoxText,
                             checkBoxManual]

          checkBoxText = UI.span # set UI.id_ "pManualMode"
                                 # set UI.name "pManualMode"
                                 # set UI.text "MANUAL MODE: "
                                 # set UI.style [("position","relative"),
                                                 ("color"     ,"white"   ),
                                                 ("text-align","center"),
                                                 ("margin-left","auto"),
                                                 ("margin-right","auto"),
                                                 ("font-size","30px"),
                                                 ("font-weight", "bold"),
                                                 ("vertical-align","middle")]

          checkBoxManual = UI.input # set UI.type_ "checkbox"
                                    # set UI.id_ "cbManualMode"
                                    # set UI.name "cbManualMode"
                                    # set UI.style [("cursor", "pointer"),
                                                    ("border-radius", "1px"),
                                                    ("box-sizing", "border-box"),
                                                    ("position", "relative"),
                                                    ("margin-left","auto"),
                                                    ("margin-right","auto"),
                                                    ("box-sizing", "content-box"),
                                                    ("width", "50px"),
                                                    ("height", "50px"),
                                                    ("border-width", "0"),
                                                    ("transition", "all .3s linear"),
                                                    ("vertical-align","middle")
                                                    ]
                                  
          elems = [mainTitle,
                   secondTitle,
                   cbSelectMap,
                   btnLaunchMap,
                   thirdTitle,
                   cbSelectCode,
                   btnExecAlg,
                   manual]

      elems

topPage :: FilePath -> UI Element
topPage absFolderPath = do

  scptUpdate <- UI.loadFile "application/javascript" "scripts/updateImage.js"
  updateImage <- mkElement "script" # set UI.src scptUpdate

  chart <- UI.loadFile "image/png" $ absFolderPath++"poseXY.png"
  img <- mkElement "img" # set UI.id_ "chart"
                         # set UI.src chart
                         # set UI.style [("position","relative"),
                                         ("width", "100%"),
                                         ("height", "100%")
                                        ]
                         #+ [element updateImage]

  UI.div # set UI.id_ "second"
         # set UI.style [("background-color","green"),
                         ("position","relative"),
                         ("width", "100%"),
                         ("height", "50%")
                        ]
         #+ [element img]            
    
bottomPage :: UI Element
bottomPage =  UI.div # set UI.id_ "third"
                     # set UI.style [("position","relative"),
                                     ("background-color","black"),
                                     ("display","flex"),
                                     ("flex-direction","column"),
                                     ("width","100%"),
                                     ("height","50%"),
                                     ("min-height","100px")
                                    ]
                     #+ [terminalOutput, UI.div # set UI.style [("background-color","#3A3B3A"),
                                                                ("position","relative"),
                                                                ("box-sizing", "border-box"),
                                                                ("margin","auto"),                                                           
                                                                ("height","50px"),
                                                                ("min-height","50px"),
                                                                ("max-height","50px"),
                                                                ("width", "100%"),
                                                                ("flex", "1")
                                                               ]
                                                #+ [cmdInputs]
                        ]       
  where
    terminalOutput = do 
      cd <- liftIO getCurrentDirectory
      scptScroll <- UI.loadFile "application/javascript" "scripts/autoScroll.js"
      scroll <- mkElement "script" # set UI.src scptScroll
      
      UI.p # set UI.id_ "cmdText"
           # set UI.text (cd ++ ">")
           # set UI.value (cd ++ ">")
           # set UI.style [("margin","6pt"), 
                           ("min-width","50px"),
                           ("color","white"),
                           ("font-family","Courier New"),
                           ("white-space", "pre-wrap"),
                           ("flex", "1"),
                           ("overflow-y","auto"),
                           ("word-wrap", "break-word"),
                           ("display","inline-block")
                          ]
           #+[element scroll]

    cmdInputs = UI.input # set UI.id_ "cmdForm"
                         # set UI.name "cmdForm" 
                         # set UI.type_ "text"
                         # set UI.class_ "rq-form-element"
                         # set (UI.attr "autofocus") "true"
                         # set UI.value ""
                         # set (UI.attr "placeholder") "insert command"
                         # set UI.style [("background","transparent"),
                                         ("width","100%"),
                                         ("margin","10pt"),
                                         ("border","none"),
                                         ("outline-width", "0"),
                                         ("color","white"),
                                         ("font-family","Courier New"),
                                         ("font-size","13pt"),
                                         ("flex", "1")
                                        ]
                     

separatorCol :: UI Element
separatorCol = UI.div # set UI.id_ "separatorCol"
                      # set UI.style [("cursor","col-resize"),
                                      ("background-color", "#aaa"),
                                      ("background-repeat", "no-repeat"),
                                      ("background-position", "center"),
                                      ("width", "10px"),
                                      ("height", "100%"),
                                      ("-moz-user-select", "none"),
                                      ("-ms-user-select", "none"),
                                      ("user-select", "none")]

separatorRow :: UI Element
separatorRow = UI.div # set UI.id_ "separatorRow"
                      # set UI.style [("cursor","row-resize"),
                                      ("background-color", "#aaa"),
                                      ("background-repeat", "no-repeat"),
                                      ("background-position", "center"),
                                      ("width", "100%"),
                                      ("height", "10px"),
                                      ("-moz-user-select", "none"),
                                      ("-ms-user-select", "none"),
                                      ("user-select", "none")]