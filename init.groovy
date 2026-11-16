import jenkins.model.*
import hudson.security.*

def instance = Jenkins.getInstance()

// Create admin user: admin / admin123
def hudsonRealm = new HudsonPrivateSecurityRealm(false)
hudsonRealm.createAccount('admin', 'admin123')
instance.setSecurityRealm(hudsonRealm)

// Authorization: logged in users have full control, anonymous can view
def strategy = new FullControlOnceLoggedInAuthorizationStrategy()
strategy.setAllowAnonymousRead(true)
instance.setAuthorizationStrategy(strategy)

instance.save()
println("--> Jenkins security realm and admin user configured successfully.")
