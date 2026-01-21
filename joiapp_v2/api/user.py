from joiapp_v2.security.security import get_current_user

@router.get("/userdata")
def get_user_data(
    current_user: dict = Depends(get_current_user)
):
    return {
        "email": current_user.get("email"),
        "name": current_user.get("name"),
        "data": "data"
    }

# @router.get("/admindata")
# def get_admin_data(
#     current_user: dict = Depends(require_role("admin"))
# ):
#     return {
#         "admin_info": "admin_data",
#         "sensitive_data": "info"
#     }


# user check
# @router.get("/users/by-email")
# def get_user_by_email(
#     email: str,
#     current_user: dict = Depends(get_current_user)
# ):
#     # admin email
#     if current_user.get("email") != email and current_user.get("role") != "admin":
#         raise HTTPException(403, "Access denied")
    
#     users_ref = db.collection("users").where("email", "==", email).limit(1).stream()
    
#     for user_doc in users_ref:
#         return user_doc.to_dict()
    
#     raise HTTPException(404, "User not found")