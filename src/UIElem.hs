module UIElem where

import Data.List ( sort )
import qualified Graphics.UI.Threepenny as UI
import Graphics.UI.Threepenny.Core ( MonadIO(liftIO), UI, Element, (#), (#+), set, text, value ) 

{-
Converte uma IO List para uma UI List
-}
io2uiList ::  IO [FilePath] -> UI [FilePath]
io2uiList ioList = do
  list <- liftIO ioList
  let uiList = list

  return uiList

{-
Cria a caixa de combinações com os elementos lidos na pasta "simulator/", criando uma caixa de combinações
com o nome dos arquivos disponíveis.
-}
createComboBox :: String -> IO [FilePath] -> UI Element
createComboBox id' ioList = do
  list <- io2uiList ioList
  UI.select # set UI.name id'
            # set UI.id_  id'
            # set UI.style [("margin","auto"),
                            ("display","block"),
                            ("font-size","30px"),
                            ("margin-top","20px")]
            #+ map (\name -> UI.option # set value name
                                       # set text name
                                       # set UI.style [("font-size","30px")])
                   (sort $ filter (`notElem` [".","..","README.md","__init__.py","__pycache__"]) list)

{-
Cria a interface de um botão
-}
createButton :: (String, String) -> UI Element
createButton (text, id') = UI.button # set UI.text text
                                     # set UI.id_  id'
                                     # set UI.style [("margin","auto"),
                                                     ("display","block"),
                                                     ("font-size","30px"),
                                                     ("margin-top","15px")]