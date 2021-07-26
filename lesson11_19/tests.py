from python_tests.lesson11_19.confest import app


#region TESTS_METHODS_REGION

def test_add_delete_cart_products(app):

    for i in range(3):
        app.add_product_to_cart()

    app.delete_products_in_cart()

#endregion