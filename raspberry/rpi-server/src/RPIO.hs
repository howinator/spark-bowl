module RPIO 
  ( openWaitAndClosePin
  ) where

import Control.Concurrent
import Control.Monad.Except
import System.GPIO.Monad
import System.GPIO.Linux.Sysfs

openWaitAndClosePin
  :: Int 
  -> IO () 
openWaitAndClosePin pinNum = runOperation $ do
  withOutputPin (Pin pinNum) OutputDefault Nothing High $ \h -> do
    liftIO $ threadDelay 5
    writeOutputPin h Low

runOperation :: SysfsGpioIO () -> IO () 
runOperation = void . runSysfsGpioIO
