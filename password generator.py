import random
import string

def generate_password(length=12):
    """
    Generate a random password with specified length.
    Includes uppercase, lowercase, digits, and special characters.
    """
    if length < 4:
        raise ValueError("Password length must be at least 4 characters")
    
    # Define character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Ensure at least one character from each set
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special)
    ]
    
    # Fill the rest with random characters from all sets
    all_chars = lowercase + uppercase + digits + special
    for _ in range(length - 4):
        password.append(random.choice(all_chars))
    
    # Shuffle the password to avoid predictable patterns
    random.shuffle(password)
    
    return ''.join(password)

def main():
    print("=== Password Generator ===")
    
    while True:
        try:
            length = int(input("Enter password length (minimum 4, default 12): ") or "12")
            password = generate_password(length)
            print(f"\nGenerated password: {password}")
            
            another = input("\nGenerate another password? (y/n): ").lower()
            if another != 'y':
                break
                
        except ValueError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
    
    print("Goodbye!")

if __name__ == "__main__":
    main()
