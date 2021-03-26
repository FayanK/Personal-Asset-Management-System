from django.urls import path
from . import views

app_name = 'pamsapp'

urlpatterns = [
    path('', views.index_view, name='home'),
    path('profile/', views.profile_view, name='profile'),
    path('profile-show/', views.profile_show_view, name='profile-show'),
    path('profile-edit/<int:user_id>/', views.profile_edit_view, name='profile-edit'),

    path('all-user/', views.all_user_view, name='all-user'),
    path('view-user/<int:id>', views.view_user_view, name='view-user'),
    path('view-user-all-assets/<int:user_id>/', views.user_all_assets_view, name='view-user-all-assets'),
    path('view-user-immovable/<int:user_id>/', views.view_user_immovable_view, name='view-user-immovable'),
    path('view-user-movable/<int:user_id>/', views.view_user_movable_view, name='view-user-movable'),
    
    path('edit-user/<int:id>', views.edit_user_view, name='edit-user'),
    path('delete-user/<int:id>', views.delete_user_view, name='delete-user'),

    path('designations_list/', views.all_designations_view, name='designations_list'),
    path('edit_designation/<int:id>', views.designation_edit_view, name='edit_designation'),
    path('delete_designation/<int:id>', views.delete_designation_view, name='delete_designation'),

    #Start URL of Immovable Property
    path('immovable-property/', views.immovable_properties_view, name='immovable-property'),

    path('land-add/', views.land_add_view, name='land-add'),
    path('edit-land/<int:id>', views.land_edit_view, name='edit-land'),
    path('view-land/<int:id>', views.view_land_view, name='view-land'),
    path('edit-land-admin/<int:id>', views.land_edit_admin, name='edit-land-admin'),
    path('delete-land-admin/<int:land_id>', views.land_delete_admin, name='delete-land-admin'),

    path('building-add/', views.building_add_view, name='building-add'),
    path('edit-building/<int:id>', views.building_edit_view, name='edit-building'),
    path('view-building/<int:id>', views.view_building_view, name='view-building'),
    path('edit-building-admin/<int:id>', views.building_edit_admin, name='edit-building-admin'),
    path('delete-building-admin/<int:building_id>', views.building_delete_admin, name='delete-building-admin'),

    path('homestead-add/', views.homestead_add_view, name='homestead-add'),
    path('edit-homestead/<int:id>', views.homestead_edit_view, name='edit-homestead'),
    path('view-homestead/<int:id>', views.view_homestead_view, name='view-homestead'),
    path('edit-homestead-admin/<int:id>', views.homestead_edit_admin, name='edit-homestead-admin'),
    path('delete-homestead-admin/<int:homestead_id>', views.homestead_delete_admin, name='delete-homestead-admin'),

    path('businessfirm-add/', views.businessFirm_add_view, name='businessfirm-add'),
    path('edit-businessfirm/<int:id>', views.businessFirm_edit_view, name='edit-businessfirm'),
    path('view-businessfirm/<int:id>', views.view_businessfirm_view, name='view-businessfirm'),
    path('edit-businessfirm-admin/<int:id>', views.businessFirm_edit_admin, name='edit-businessfirm-admin'),
    path('delete-businessfirm-admin/<int:businessfirm_id>', views.businessFirm_delete_admin, name='delete-businessfirm-admin'),

    path('other-add/', views.other_add_view, name='other-add'),
    path('edit-other/<int:id>', views.other_edit_view, name='edit-other'),
    path('view-other/<int:id>', views.view_other_view, name='view-other'),
    path('edit-other-admin/<int:id>', views.other_edit_admin, name='edit-other-admin'),
    path('delete-other-admin/<int:other_id>', views.other_delete_admin, name='delete-other-admin'),

    #movable property
    path('movable-property/', views.movable_properties_view, name='movable-property'),

    path('ornaments-add/', views.ornaments_add_view, name='ornaments-add'),
    path('edit-ornaments/<int:id>', views.ornaments_edit_view, name='edit-ornaments'),
    path('edit-ornaments-admin/<int:id>', views.ornaments_edit_admin, name='edit-ornaments-admin'),
    path('delete-ornaments-admin/<int:ornament_id>', views.ornaments_delete_admin, name='delete-ornaments-admin'),

    path('stocks-add/', views.stocks_add_view, name='stocks-add'),
    path('edit-stocks/<int:id>', views.stocks_edit_view, name='edit-stocks'),

    path('shares-add/', views.shares_add_view, name='shares-add'),
    path('edit-shares/<int:id>', views.shares_edit_view, name='edit-shares'),

    path('incurances-add/', views.insurances_add_view, name='incurances-add'),
    path('edit-incurances/<int:id>', views.insurances_edit_view, name='edit-incurances'),

    path('cash-or-bankvalue-add/', views.cash_or_bankvalue_add_view, name='cash-or-bankvalue-add'),
    path('edit-cash-or-bankvalue/<int:id>', views.cash_or_bankvalue_edit_view, name='edit-cash-or-bankvalue'),

    path('vehicles-add/', views.vehicles_add_view, name='vehicles-add'),
    path('edit-vehicles/<int:id>', views.vehicles_edit_view, name='edit-vehicles'),

    path('electronics-add/', views.electronics_add_view, name='electronics-add'),
    path('edit-electronics/<int:id>', views.electronics_edit_view, name='edit-electronics'),

    path('other-m-add/', views.other_m_add_view, name='other-m-add'),
    path('edit-other-m/<int:id>', views.other_m_edit_view, name='edit-other-m'),

    path('show-properties/', views.show_properties_view, name='show-properties'),
    
    path('dashboard/', views.dashboard_view, name='dashboard'),

    path('assets-list/', views.assets_list_view, name='assets-list'),
    path('assets-list-pending/', views.assets_list_pending_view, name='assets-list-pending'),
    # chatroom 
    # path('chatroom/<int:pk>', views.chatroom_view, name='chatroom'),
    # path('ajax/<int:pk>', views.ajax_load_message, name = 'chatroom-ajax') 
    path("chatroom/<int:pk>/", views.chatroom, name="chatroom"),
    path("ajax/<int:pk>/", views.ajax_load_messages, name="chatroom-ajax"),
]







