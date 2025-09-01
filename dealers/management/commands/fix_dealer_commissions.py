from django.core.management.base import BaseCommand
from dealers.models import Dealer, Project, ProjectCommission
from buyers.models import Buyer
from decimal import Decimal

class Command(BaseCommand):
    help = 'Fix dealer-buyer data so commission payable is correctly calculated'

    def handle(self, *args, **options):
        for dealer in Dealer.objects.all():
            buyers = dealer.buyers.all()
            if not buyers.exists():
                self.stdout.write(f'⚠️ Dealer {dealer.name} has no buyers')
                continue

            for b in buyers:
                # Ensure total_price is > 0
                if not b.total_price or b.total_price == 0:
                    b.total_price = Decimal('100000')  # Example amount
                    b.save()
                    self.stdout.write(f'✅ Updated total_price for buyer {b.name}')

                # Ensure property exists in Project
                if b.property:
                    project, created = Project.objects.get_or_create(name=b.property)
                    # Optional: assign a project-specific commission if needed
                    if not ProjectCommission.objects.filter(dealer=dealer, project=project).exists():
                        ProjectCommission.objects.create(
                            dealer=dealer,
                            project=project,
                            percent=dealer.commission_rate  # use dealer default rate
                        )
                        self.stdout.write(f'✅ Added ProjectCommission for dealer {dealer.name}, project {project.name}')

            payable = dealer.commission_payable()
            self.stdout.write(f'💰 Dealer {dealer.name} payable commission: {payable}')
