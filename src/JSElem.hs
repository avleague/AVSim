{-# LANGUAGE QuasiQuotes, OverloadedStrings #-}
module JSElem where

import Language.Javascript.JMacro

testExample :: JStat
testExample = [jmacro|
                document.location.href="http://google.com";
              |]

currentDirectory :: JStat
currentDirectory = [jmacro|
                     var loc = window.location.pathname;
                     console.log(window.location.pathname);
                   |]

executeScroll :: JStat
executeScroll = [jmacro|
                 runGetMessages();
                |]

