from mail_haven import MailHaven, Documentation

def test_deployment_guide():
    documentation = Documentation(
        deployment_guide='Step-by-step deployment guide is available',
        troubleshooting_guide='Troubleshooting guide is included',
        support_channels=['Email', 'Phone', 'Chat']
    )
    mail_haven = MailHaven(documentation)
    assert mail_haven.get_deployment_guide() == 'Step-by-step deployment guide is available'

def test_troubleshooting_guide():
    documentation = Documentation(
        deployment_guide='Step-by-step deployment guide is available',
        troubleshooting_guide='Troubleshooting guide is included',
        support_channels=['Email', 'Phone', 'Chat']
    )
    mail_haven = MailHaven(documentation)
    assert mail_haven.get_troubleshooting_guide() == 'Troubleshooting guide is included'

def test_support_channels():
    documentation = Documentation(
        deployment_guide='Step-by-step deployment guide is available',
        troubleshooting_guide='Troubleshooting guide is included',
        support_channels=['Email', 'Phone', 'Chat']
    )
    mail_haven = MailHaven(documentation)
    assert mail_haven.get_support_channels() == ['Email', 'Phone', 'Chat']
