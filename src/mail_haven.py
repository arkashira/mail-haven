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
    parser.add_argument('--deployment-guide', action='store_true', help='Print deployment guide')
    parser.add_argument('--troubleshooting-guide', action='store_true', help='Print troubleshooting guide')
    parser.add_argument('--support-channels', action='store_true', help='Print support channels')
    args = parser.parse_args()

    documentation = Documentation(
        deployment_guide='Step-by-step deployment guide is available',
        troubleshooting_guide='Troubleshooting guide is included',
        support_channels=['Email', 'Phone', 'Chat']
    )

    mail_haven = MailHaven(documentation)

    if args.deployment_guide:
        print(mail_haven.get_deployment_guide())
    elif args.troubleshooting_guide:
        print(mail_haven.get_troubleshooting_guide())
    elif args.support_channels:
        print(mail_haven.get_support_channels())
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
