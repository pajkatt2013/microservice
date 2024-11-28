import time

# Step 1: Define the decorator function
def timer(func):
    # Step 2: Define the wrapper function
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Record the start time
        result = func(*args, **kwargs)  # Call the original function
        end_time = time.time()  # Record the end time
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds to execute")  # Print the elapsed time
        return result  # Return the result of the original function
    
    # Step 3: Return the wrapper function
    return wrapper

# Step 4: Apply the decorator using the @ syntax
@timer
def example_function():
    for _ in range(1000000):
        pass  # Simulate a time-consuming task
    print("done!")

# Step 5: Call the decorated function
example_function()
