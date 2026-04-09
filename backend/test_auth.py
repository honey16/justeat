from app.database import SessionLocal
from app.models import User
from app.auth import verify_password, get_password_hash

db = SessionLocal()

print("\n" + "="*50)
print("Testing Authentication")
print("="*50 + "\n")

# Check customer
customer = db.query(User).filter(User.email == "customer@test.com").first()
if customer:
    print(f"✓ Customer found: {customer.email}")
    print(f"  Role: {customer.role}")
    print(f"  Stored hash: {customer.hashed_password[:60]}...")
    
    # Test password
    test_password = "123456"
    print(f"\n  Testing password: '{test_password}'")
    
    try:
        result = verify_password(test_password, customer.hashed_password)
        print(f"  ✓ Password verification: {result}")
        
        if not result:
            print("\n  ⚠ Password doesn't match! Resetting...")
            new_hash = get_password_hash(test_password)
            customer.hashed_password = new_hash
            db.commit()
            print(f"  ✓ Password reset successfully")
            print(f"  New hash: {new_hash[:60]}...")
            
            # Verify again
            result2 = verify_password(test_password, customer.hashed_password)
            print(f"  ✓ Re-verification: {result2}")
    except Exception as e:
        print(f"  ✗ Error: {e}")
        print("\n  Resetting password...")
        new_hash = get_password_hash(test_password)
        customer.hashed_password = new_hash
        db.commit()
        print(f"  ✓ Password reset successfully")
else:
    print("✗ Customer not found!")

print("\n" + "="*50)

# Check owner
owner = db.query(User).filter(User.email == "owner@test.com").first()
if owner:
    print(f"✓ Owner found: {owner.email}")
    print(f"  Role: {owner.role}")
    print(f"  Stored hash: {owner.hashed_password[:60]}...")
    
    test_password = "123456"
    print(f"\n  Testing password: '{test_password}'")
    
    try:
        result = verify_password(test_password, owner.hashed_password)
        print(f"  ✓ Password verification: {result}")
        
        if not result:
            print("\n  ⚠ Password doesn't match! Resetting...")
            new_hash = get_password_hash(test_password)
            owner.hashed_password = new_hash
            db.commit()
            print(f"  ✓ Password reset successfully")
            print(f"  New hash: {new_hash[:60]}...")
            
            result2 = verify_password(test_password, owner.hashed_password)
            print(f"  ✓ Re-verification: {result2}")
    except Exception as e:
        print(f"  ✗ Error: {e}")
        print("\n  Resetting password...")
        new_hash = get_password_hash(test_password)
        owner.hashed_password = new_hash
        db.commit()
        print(f"  ✓ Password reset successfully")
else:
    print("✗ Owner not found!")

print("\n" + "="*50)
print("✅ Test Complete!")
print("="*50)
print("\nYou can now login with:")
print("  customer@test.com / 123456")
print("  owner@test.com / 123456")
print()

db.close()
