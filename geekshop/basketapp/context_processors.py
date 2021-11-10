from basketapp.models import Basket


def basket(request):
    print('context_processor "basket" works!')

    context_basket = []

    if request.user.is_authenticated:
        context_basket = Basket.objects.filter(user=request.user)

    return {
        'basket': context_basket,
    }
