from app import app, indexbp
from app.accounts.controllers import accountsbp
from app.login.controllers import loginbp
from app.positions.controllers import positionsbp
from app.profile.controllers import profilebp
from app.create.controllers import createbp
from app.pending.controllers import pendingbp
from app.reports.controllers import reportsbp

app.register_blueprint(accountsbp)
app.register_blueprint(indexbp)
app.register_blueprint(loginbp)
app.register_blueprint(positionsbp)
app.register_blueprint(profilebp)
app.register_blueprint(createbp)
app.register_blueprint(pendingbp)
app.register_blueprint(reportsbp)