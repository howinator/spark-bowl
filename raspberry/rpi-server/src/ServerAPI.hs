{-# LANGUAGE OverloadedStrings #-}
{-# LANGUAGE DataKinds #-}
{-# LANGUAGE DeriveGeneric #-}
{-# LANGUAGE FlexibleInstances #-}
{-# LANGUAGE GeneralizedNewtypeDeriving #-}
{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE RecordWildCards #-}
{-# LANGUAGE ScopedTypeVariables #-}
{-# LANGUAGE TypeOperators #-}

module ServerAPI
  ( runServer
  ) where

import Prelude ()
import Prelude.Compat

import Types

import Control.Monad.Except
import Control.Monad.Reader
import Data.Attoparsec.ByteString
import Data.ByteString (ByteString)
import Data.List
import Data.Maybe
import Data.Text
import Data.String.Conversions
import Data.Time.Calendar
import Data.Time.Clock.POSIX
import GHC.Generics
import Lucid
import Network.Wai
import Network.Wai.Handler.Warp
import Servant
import qualified Data.Aeson.Parser

type RPiAPI = "user-intent" :> ReqBody '[JSON] UserIntent :> Post '[JSON] String 

validateIntentRequest :: UserIntent -> IO ValidationResult
validateIntentRequest Intent{..} = 
  case intentType of 
    "FeedDogsNow" -> do
      timeout <- hitsTimeout timestamp
      return $ if timeout then Failure else Success
    _ -> return Failure
  where
    hitsTimeout :: Int -> IO Bool
    hitsTimeout ts = do
      now <- round <$> getPOSIXTime
      return $ (now - ts) > 5 

intentRequestHandler :: UserIntent -> Handler String
intentRequestHandler req = do
  validationRes <- liftIO $ validateIntentRequest req
  case validationRes of 
    -- TODO: Add RPIO here upon success
    Success -> return "SUCCESS" 
    Failure -> throwError err503

-- Necessary boilerplate to satisfy type system
rpiAPI :: Proxy RPiAPI
rpiAPI = Proxy

server :: Server RPiAPI
server = intentRequestHandler

app :: Application
app = serve rpiAPI server

runServer :: IO ()
runServer = run 3001 app 
