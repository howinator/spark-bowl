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

import RPIO
import Types

import qualified Control.Exception as E
import Control.Monad.Except
import Data.ByteString.Lazy.Char8
import Data.Time.Clock.POSIX
import Network.Wai
import Network.Wai.Handler.Warp
import Servant
import System.GPIO.Monad

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

getActionForRequest :: UserIntent -> IO ()
getActionForRequest Intent{..} = 
  case intentType of 
    "FeedDogsNow" -> openWaitAndClosePin 25
    _ -> return ()

intentRequestHandler :: UserIntent -> Handler String
intentRequestHandler req = do
  validationResult <- liftIO $ validateIntentRequest req
  case validationResult of 
    Success -> handlePinOperation $ getActionForRequest req
    Failure -> throwError $ err500 { errBody = "Invalid Request" }

handlePinOperation :: IO () -> Handler String
handlePinOperation operation = do
  opOrError <- liftIO operationOrError
  case opOrError of
    Left e -> throwError $ err500 { errBody = pack (E.displayException e) }
    Right _ -> return "SUCCESS"
  where
    operationOrError :: IO (Either SomeGpioException ())
    operationOrError = E.try operation

-- Necessary boilerplate to satisfy type system
rpiAPI :: Proxy RPiAPI
rpiAPI = Proxy

server :: Server RPiAPI
server = intentRequestHandler

app :: Application
app = serve rpiAPI server

runServer :: IO ()
runServer = run 3001 app 
