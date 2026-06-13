import json
from dataclasses import dataclass
from argparse import ArgumentParser

@dataclass
class Documentation:
    deployment_guide: str
    troubleshooting_guide: str
    support_channels: list

class MailHaven:
    def __init__(self, documentation: Documentation):
        self.documentation = documentation

    def get_deployment_guide(self):
        return self.documentation.deployment_guide

    def get_troubleshooting_guide(self):
        return self.documentation.troubleshooting_guide

    def get_support_channels(self):
        return self.documentation.support_channels

def main():
    parser = ArgumentParser(description='Mail Haven Documentation and Support')
    parser.add_argument('--deployment-guide', help='Step-by-step deployment guide')
    parser.add_argument('--troubleshooting-guide', help='Troubleshooting guide')
    parser.add_argument('--support-channels', nargs='+', help='Basic support channels')
    args = parser.parse_args()

    documentation = Documentation(
        deployment_guide=args.deployment_guide,
        troubleshooting_guide=args.troubleshooting_guide,
        support_channels=args.support_channels
    )

    mail_haven = MailHaven(documentation)

    print('Deployment Guide:')
    print(mail_haven.get_deployment_guide())
    print('Troubleshooting Guide:')
    print(mail_haven.get_troubleshooting_guide())
    print('Support Channels:')
    print(mail_haven.get_support_channels())

if __name__ == '__main__':
    main()
