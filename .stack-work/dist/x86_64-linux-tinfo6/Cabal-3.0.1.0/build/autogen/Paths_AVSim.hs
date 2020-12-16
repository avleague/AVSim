{-# LANGUAGE CPP #-}
{-# LANGUAGE NoRebindableSyntax #-}
{-# OPTIONS_GHC -fno-warn-missing-import-lists #-}
module Paths_AVSim (
    version,
    getBinDir, getLibDir, getDynLibDir, getDataDir, getLibexecDir,
    getDataFileName, getSysconfDir
  ) where

import qualified Control.Exception as Exception
import Data.Version (Version(..))
import System.Environment (getEnv)
import Prelude

#if defined(VERSION_base)

#if MIN_VERSION_base(4,0,0)
catchIO :: IO a -> (Exception.IOException -> IO a) -> IO a
#else
catchIO :: IO a -> (Exception.Exception -> IO a) -> IO a
#endif

#else
catchIO :: IO a -> (Exception.IOException -> IO a) -> IO a
#endif
catchIO = Exception.catch

version :: Version
version = Version [0,1,0,0] []
bindir, libdir, dynlibdir, datadir, libexecdir, sysconfdir :: FilePath

bindir     = "/mnt/c/Users/GilmarCorreia/Documents/Documentos/Projetos/GitHub/UFABC GIT/Paradigmas_de_Programa\231\227o/2020-qs-paradigmas-diurno-projetofinal-GilmarCorreia/AVSim/.stack-work/install/x86_64-linux-tinfo6/7aa1ffd653b4f966d9ff13a77eb8fe6a3c18cd4d853fb450ed1e4eec5508d4ec/8.8.4/bin"
libdir     = "/mnt/c/Users/GilmarCorreia/Documents/Documentos/Projetos/GitHub/UFABC GIT/Paradigmas_de_Programa\231\227o/2020-qs-paradigmas-diurno-projetofinal-GilmarCorreia/AVSim/.stack-work/install/x86_64-linux-tinfo6/7aa1ffd653b4f966d9ff13a77eb8fe6a3c18cd4d853fb450ed1e4eec5508d4ec/8.8.4/lib/x86_64-linux-ghc-8.8.4/AVSim-0.1.0.0-7VAn0fL7U8OHBLIVjqxPin"
dynlibdir  = "/mnt/c/Users/GilmarCorreia/Documents/Documentos/Projetos/GitHub/UFABC GIT/Paradigmas_de_Programa\231\227o/2020-qs-paradigmas-diurno-projetofinal-GilmarCorreia/AVSim/.stack-work/install/x86_64-linux-tinfo6/7aa1ffd653b4f966d9ff13a77eb8fe6a3c18cd4d853fb450ed1e4eec5508d4ec/8.8.4/lib/x86_64-linux-ghc-8.8.4"
datadir    = "/mnt/c/Users/GilmarCorreia/Documents/Documentos/Projetos/GitHub/UFABC GIT/Paradigmas_de_Programa\231\227o/2020-qs-paradigmas-diurno-projetofinal-GilmarCorreia/AVSim/.stack-work/install/x86_64-linux-tinfo6/7aa1ffd653b4f966d9ff13a77eb8fe6a3c18cd4d853fb450ed1e4eec5508d4ec/8.8.4/share/x86_64-linux-ghc-8.8.4/AVSim-0.1.0.0"
libexecdir = "/mnt/c/Users/GilmarCorreia/Documents/Documentos/Projetos/GitHub/UFABC GIT/Paradigmas_de_Programa\231\227o/2020-qs-paradigmas-diurno-projetofinal-GilmarCorreia/AVSim/.stack-work/install/x86_64-linux-tinfo6/7aa1ffd653b4f966d9ff13a77eb8fe6a3c18cd4d853fb450ed1e4eec5508d4ec/8.8.4/libexec/x86_64-linux-ghc-8.8.4/AVSim-0.1.0.0"
sysconfdir = "/mnt/c/Users/GilmarCorreia/Documents/Documentos/Projetos/GitHub/UFABC GIT/Paradigmas_de_Programa\231\227o/2020-qs-paradigmas-diurno-projetofinal-GilmarCorreia/AVSim/.stack-work/install/x86_64-linux-tinfo6/7aa1ffd653b4f966d9ff13a77eb8fe6a3c18cd4d853fb450ed1e4eec5508d4ec/8.8.4/etc"

getBinDir, getLibDir, getDynLibDir, getDataDir, getLibexecDir, getSysconfDir :: IO FilePath
getBinDir = catchIO (getEnv "AVSim_bindir") (\_ -> return bindir)
getLibDir = catchIO (getEnv "AVSim_libdir") (\_ -> return libdir)
getDynLibDir = catchIO (getEnv "AVSim_dynlibdir") (\_ -> return dynlibdir)
getDataDir = catchIO (getEnv "AVSim_datadir") (\_ -> return datadir)
getLibexecDir = catchIO (getEnv "AVSim_libexecdir") (\_ -> return libexecdir)
getSysconfDir = catchIO (getEnv "AVSim_sysconfdir") (\_ -> return sysconfdir)

getDataFileName :: FilePath -> IO FilePath
getDataFileName name = do
  dir <- getDataDir
  return (dir ++ "/" ++ name)
