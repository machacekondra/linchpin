#!/usr/bin/env python
print "Linchpin Testing Initiating..."

print "Testing Linchpin TestClass: TestLinchpinInvocation" 
from test_linchpin_invocation import TestLinchPinInvocation

print "Testing Linchpin TestClass: TestLinchpinCredentials"
from test_linchpin_creds import TestLinchPinCredentials

print "Testing Linchpin TestClass: TestLinchpinEnv"
from test_linchpin_env import TestLinchPinEnv

import nose
nose.run()
