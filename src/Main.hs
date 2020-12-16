module Main where

-- Módulos criados para o projeto: 
import JSElem 
import Pages

-- Módulos importados:
import Language.Javascript.JMacro
import Control.Monad
import Control.Exception 
import Control.Concurrent
import Control.Concurrent.Async
import Data.Char
import System.Exit
import System.Process
import System.Process.Internals
import System.Directory
import System.IO
import System.FilePath.Windows
import qualified Graphics.UI.Threepenny as UI
import Graphics.UI.Threepenny.Core

-- Três tipos de dados foram criados para executar os programas na ordem correta
type UnrealEnv = String
type UnrealProgram = String
type CodeName = String

-- main inicializa a GUI
main :: IO ()
main = startGUI defaultConfig {jsLog = \_ -> return ()} setup

-- setup monta a estrutura da GUI
setup :: Window -> UI()
setup window = void $ do
  -- Título da página 
  return window # set title "AVSim"

  -- Salva o diretório do projeto na função absoluteFolderPath e o diretório do simulador na função simFolderPath  
  absoluteFolderPath <- liftIO getCurrentDirectory
  let simFolderPath = absoluteFolderPath ++ "/simulator/"

  
  -- Carrega o diretório para utilizar os arquivos presentes neles
  UI.loadDirectory simFolderPath

  -- Monta todo HTML e CSS da pagina principal
  mainScreen <- UI.div # set UI.style [("width","100%"),
                                       ("height","calc(100% - 25pt)"),
                                       ("position","absolute"),
                                       ("display","flex")
                                      ]
                       #+ [leftPage, separatorCol,
                           UI.div  # set UI.id_ "rightPane"
                                   # set style [("position","relative"),
                                                ("width","50%"),
                                                ("min-width","100px"),
                                                ("height","100%"),
                                                ("display","flex"),
                                                ("flex-direction","column")]
                                   #+ [topPage simFolderPath, separatorRow, bottomPage]
                          ]

  poweredBy <- UI.mkElement "footer" # set UI.id_ "footer"
                                     # set UI.style [("position","fixed"),
                                                     ("width","100%"),
                                                     ("height","25pt"),
                                                     ("display","block"),
                                                     ("margin", "auto"),
                                                     ("align-items", "center"),
                                                     ("background-color","#1f1f1f"),
                                                     ("border-top","3px solid white"),
                                                     ("text-align", "center"),
                                                     ("flex","1"),
                                                     ("bottom","0"),
                                                     ("vertical-align","middle")
                                                    ]   
                                     #+ [UI.a # set UI.text "powered by Autonomous Vehicle League"
                                              # set UI.href "https://avleague.github.io/pt/"
                                              # set (UI.attr "target") "_blank"
                                              # set UI.style [("color","white"),
                                                              ("margin-right", "25px"),
                                                              ("display","block"),
                                                              ("vertical-align","middle"),
                                                              ("text-align", "center"),
                                                              ("float","right"),
                                                              ("font-family","Courier New")
                                                              ]
                                        ]               
                         
  -- Adiciona os scripts de resize.js
  scptResize <- UI.loadFile "application/javascript" "scripts/resize.js"
  resize <- mkElement "script" # set UI.src scptResize

  -- Agrupa todos os elementos para uma única tela e envia para o window
  getBody window #+ [element mainScreen,
                     element poweredBy,
                     element resize
                    ]
                 # set UI.style [("margin","0"),
                                 ("padding","0"),
                                 ("overflow", "hidden")]

  -- Instala as dependências do projeto, se já tiver instalado, não executa as funções
  depInstall <- liftIO $ doesFileExist $ absoluteFolderPath ++ "/depInstalled.txt"
  
  unless depInstall $ do
    liftIO $ tryCommand window "pip install numpy"
    liftIO $ tryCommand window "pip install matplotlib"
    liftIO $ tryCommand window "pip install airsim"
    liftIO $ tryCommand window $ "mkdir " ++ concat (take 3 $ splitPath absoluteFolderPath) ++"Documents\\AirSim"
    liftIO $ tryCommand window $ "copy " ++ absoluteFolderPath ++ "\\simulator\\json\\settings.json " ++ 
                         concat (take 3 $ splitPath absoluteFolderPath) ++ "Documents\\AirSim\\"
    liftIO $ tryCommand window "type nul > depInstalled.txt"
    runFunction $ ffi $ show $ renderJs executeScroll


  -- Ativação dos comandos JS
  
  {-
  Seleciona o elemento com ID btnLaunchMap, quando o botão é clicado verifica-se o ambiente unreal
  selecionado na caixa de combinações de id cbSelectMap. Posteriormente executa a função launchMap
  e a função contida no script executeScroll da JSElem.hs
  -}

  btn <- getElementById window "btnLaunchMap"
  on UI.click (unbox btn) $ \_ -> do
    cbMap <- getElementById window "cbSelectMap"
    selectedMap <- get UI.value (unbox cbMap)
    launchMap window simFolderPath selectedMap

    runFunction $ ffi $ show $ renderJs executeScroll
  
  {-
  Seleciona o elemento com ID btnExecMap, quando o botão é clicado verifica-se o ambiente unreal
  selecionado na caixa de combinações de id cbSelectMap, o código a ser executado selecionado pela
  caixa de combinações de id cdSelectCode e verifica o modo que está sendo executado, se é o MANUAL
  ou AUTO. Posteriormente executa a função launchCode e a função contida no script executeScroll da 
  JSElem.hs
  -}

  btn2 <- getElementById window "btnExecAlg"
  on UI.click (unbox btn2) $ \_ -> do
    cbMap <- getElementById window "cbSelectMap"
    selectedMap <- get UI.value (unbox cbMap)

    cbCode <- getElementById window "cbSelectCode"
    selectedCode <- get UI.value (unbox cbCode)

    cbManual <- getElementById window "cbManualMode"
    selectedManual <- get UI.checked (unbox cbManual)

    launchCode window simFolderPath selectedMap selectedCode selectedManual 
    
    --printBox window " Launch another Code!"

    runFunction $ ffi $ show $ renderJs executeScroll
  
  {-
  cmdForm verifica se algum elemento foi digitado pelo usuário. Quando este recebe o carácter ENTER
  a função pega os valores digitado pelo usuário e aplica os comandos na função tryDirectory quando o
  primeiro elemento é um "cd" ou a função tryCommand. Posteriormente executa a função contida no script 
  executeScroll da JSElem.hs, para habilitar a rolagem do terminal emulado.
  -}
  cmdForm <- getElementById window "cmdForm"
  on UI.keydown (unbox cmdForm) $ \c -> when (c == 13) $ 
    do
      cmdText <- get UI.value (unbox cmdForm)
      return (unbox cmdForm) # set UI.value ""
      
      let textSplit = words cmdText

      if head textSplit == "cd" then
        tryDirectory window cmdText
      else
        liftIO $ tryCommand window cmdText

      runFunction $ ffi $ show $ renderJs executeScroll
  
  on UI.disconnect window $ const $ liftIO $ do
    setCurrentDirectory absoluteFolderPath 


-- unbox extraí os valores de um tipo Maybe a
unbox :: Maybe a -> a
unbox (Just x) = x

-- unrealProgram recebe uma String com o nome da pasta selecionada e retorna o nome do executável a ser executado pela GUI.
unrealProgram :: UnrealEnv -> UnrealProgram
unrealProgram ue
  | ue == "Africa"       = "Africa_001"
  | ue == "City"         = "CityEnviron"
  | ue == "Neighborhood" = "AirSimNH"
  | ue == "RacingTest1"  = "CityEnviron"
  | ue == "SimpleMaze"   = "Car_Maze"
  | otherwise = ue

{- 
launchMap recebe a window da GUI, o FilePath do Simulador e o UnrealEnv selecionado pela caixa de combinações. Assim executa-se
a função tryDirectory e abre o ambiente unreal com o runCommand cmd. O programa apresenta alguns parâmetros que podem ser editados
como a resolução e o formato de exibição.
-}
launchMap :: Window -> FilePath -> UnrealEnv -> UI ()
launchMap window simFolderPath ue = do
  let path = "cd " ++ simFolderPath ++ "UnrealEnvironments/" ++ ue ++ "/"
      cmd = "START " ++unrealProgram ue ++ resolution ++ parameters

  tryDirectory window path   

  printBox window $ " " ++ cmd ++ "\n"
  liftIO $ runCommand cmd

  return ()
  where
    resolution = " -ResX=640 -ResY=480"
    parameters = " -windowed"

{- 
launchCode recebe a window da GUI, o FilePath do Simulador, o UnrealEnv e o CodeName selecionado pela caixa de combinações, assim 
como o resultado da caixa de seleção MANUAL/AUTO. Assim executa-se a função tryDirectory que seleciona o path de execução, e a função
tryCommand que executa o código em python. Em comentário uma possível implementação para execução em um ambiente conda.
-}
launchCode :: Window -> FilePath -> UnrealEnv -> CodeName -> Bool -> UI ()
launchCode window simFolderPath ue cn mode = do
  let path = "cd " ++ simFolderPath
      cmd = "python -u Run.py " ++ cn ++ " " ++ unrealProgram ue ++ " " ++ if mode then "MANUAL" else "AUTO"
      --cmd3 = "conda activate avl & python Run.py " ++ cn ++ " " ++ unrealProgram ue ++ " " ++ if mode then "MANUAL" else "AUTO"
  
  tryDirectory window path  
  liftIO $ tryCommand window cmd

  return ()

{-
printBox atualiza o elemento cmdText com o texto do comando executado, e imprime o diretório no final
-}
printBox :: Window -> String -> UI ()
printBox window arg = do
  parText <- getElementById window "cmdText"
  cd <- liftIO getCurrentDirectory
  cmdOldText <- get UI.value (unbox parText)
  let cmdNewText = cmdOldText ++ arg ++ "\n" ++ cd ++ ">"

  return (unbox parText) # set UI.text cmdNewText
                         # set UI.value cmdNewText

  return ()

{-
updateBox atualiza o elemento cmdText com o texto do comando executado.
-}
updateBox :: Window -> String -> UI ()
updateBox window arg = do
  parText <- getElementById window "cmdText"
  _ <- liftIO getCurrentDirectory
  cmdOldText <- get UI.value (unbox parText)
  return (unbox parText) # set UI.text  (cmdOldText ++ arg )
                         # set UI.value (cmdOldText ++ arg )

  return ()

{-
tryDirectory testa se o comando mandado para o terminal produz algum erro, tratando o erro caso aconteça algum.
-}
tryDirectory :: Window -> String -> UI ()
tryDirectory window cmdText = do
  updateBox window $ " " ++ cmdText ++ "\n" 
  runFunction $ ffi $ show $ renderJs executeScroll

  result <- (liftIO $ try (setCurrentDirectory $ concat $ tail (words cmdText))) :: UI (Either IOException ())
  case result of
    Left exc -> printBox window $ show exc ++ "\n"
    Right _ -> printBox window ""

{-
tryCommand testa se o comando mandado para o terminal produz algum erro, tratando o erro caso aconteça algum.
-}
tryCommand :: Window -> String -> IO ()
tryCommand window cmdText = do  
  let config = (shell cmdText) {
    std_in = CreatePipe,
    std_out = CreatePipe,
    std_err = CreatePipe,
    --create_new_console = True,
    create_group = True
    --use_process_jobs = True
  }
  runUI window $ updateBox window $ " " ++ cmdText ++ "\n" 
  runUI window $ runFunction $ ffi $ show $ renderJs executeScroll

  result <- try (createProcess config)  :: IO (Either IOException (Maybe Handle, Maybe Handle, Maybe Handle,ProcessHandle))
  case result of
    Left exc -> do
      runUI window $ printBox window $ show exc ++ "\n"

    Right (Just inp , Just out, Just err, pid) -> do
      a2 <- async $ getLineCmd window pid out err
      a1 <- async $ runUI window $ getInput window pid inp a2
      wait a1
      wait a2

getInput :: Window -> ProcessHandle -> Handle -> Async() -> UI ()
getInput window ph stdin' a2 = loop
  where 
    loop = do   
      cmdForm <- getElementById window "cmdForm"
      text <- get UI.value (unbox cmdForm)
      
      isFinished <- liftIO $ getProcessExitCode ph

      when (length text > 1) $ do
        when (ord (last text) == 32) $ do
          when (init text == "\\z" || init text == "\\c") $ do
            --pid <- liftIO $ getPid ph
            --liftIO $ createProcess (shell $ "taskkill /F /PID "++ show (unbox pid))
            liftIO $ print "Process has been terminated" 
            return (unbox cmdForm) # set UI.value ""

            liftIO $ interruptProcessGroupOf ph
            liftIO $ cancel a2
            return ()

      case isFinished of
        Nothing -> loop
        Just _ -> return ()

{- 
Função teste usada para tentar plotar os comandos do terminal em paralelo
-}
getLineCmd :: Window -> ProcessHandle -> Handle -> Handle -> IO()
getLineCmd window ph stdout' stderr' = loop 
  where 
    loop = do 

      textOut <- try (hGetLine stdout') :: IO (Either IOException String)

      case textOut of
        Left _ -> do
          lastText1 <- hGetContents stdout'
          lastText2 <- hGetContents stderr'
          runUI window $ printBox window $ lastText1 <> lastText2 <> "\n"
          runUI window $ runFunction $ ffi $ show $ renderJs executeScroll

        Right text -> do
          runUI window $ updateBox window $ text ++ "\n"
          runUI window $ runFunction $ ffi $ show $ renderJs executeScroll

          isFinished <- getProcessExitCode ph

          case isFinished of
            Nothing -> loop
            Just _ -> do 
              lastText1 <- hGetContents stdout'
              lastText2 <- hGetContents stderr'
              runUI window $ printBox window $ lastText1 <> lastText2 <> "\n"
              runUI window $ runFunction $ ffi $ show $ renderJs executeScroll

          return ()
