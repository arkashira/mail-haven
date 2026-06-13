from mail_haven import MailHaven, Documentation

def test_deployment_guide():
    documentation = Documentation(
        deployment_guide='Step-by-step deployment guide',
        troubleshooting_guide='Troubleshooting guide',
        support_channels=['support@example.com']
    )
    mail_haven = MailHaven(documentation)
    assert mail_haven.get_deployment_guide() == 'Step-by-step deployment guide'

def test_troubleshooting_guide():
    documentation = Documentation(
        deployment_guide='Step-by-step deployment guide',
        troubleshooting_guide='Troubleshooting guide',
        support_channels=['support@example.com']
    )
    mail_haven = MailHaven(documentation)
    assert mail_haven.get_troubleshooting_guide() == 'Troubleshooting guide'

def test_support_channels():
    documentation = Documentation(
        deployment_guide='Step-by-step deployment guide',
        troubleshooting_guide='Troubleshooting guide',
        support_channels=['support@example.com', 'support2@example.com']
    )
    mail_haven = MailHaven(documentation)
    assert mail_haven.get_support_channels() == ['support@example.com', 'support2@example.com']
