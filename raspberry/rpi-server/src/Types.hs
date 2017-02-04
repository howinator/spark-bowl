{-# LANGUAGE OverloadedStrings #-}
module Types where

import Data.Aeson

-- TODO: Create ADT for intentType for more comprehensive pattern matching
data UserIntent = Intent 
  { intentType :: String
  , timestamp :: Int
  }

instance FromJSON UserIntent where
  parseJSON (Object v) = 
    Intent <$>
    v .: "type" <*>
    v .: "timestamp"

data ValidationResult = Success | Failure deriving (Eq)
