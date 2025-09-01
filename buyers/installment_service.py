from datetime import date, timedelta
from .models import Installment

def generate_installment_schedule(buyer):
    """
    Auto-generate installment schedule for a buyer.
    """
    # Delete old installments if regenerating
    buyer.installments.all().delete()

    num_installments = buyer.installment_plan
    if num_installments == 0:
        return

    # Remaining price after advance
    remaining_amount = buyer.total_price - buyer.advance
    per_installment = remaining_amount / num_installments

    # Example: Monthly installments starting 1 month after creation
    start_date = date.today() + timedelta(days=30)

    installments = []
    for i in range(num_installments):
        inst = Installment(
            buyer=buyer,
            amount=per_installment,
            date=start_date + timedelta(days=30 * i),  # monthly gap
            status="Pending",
            mode="Cash"
        )
        installments.append(inst)

    Installment.objects.bulk_create(installments)
