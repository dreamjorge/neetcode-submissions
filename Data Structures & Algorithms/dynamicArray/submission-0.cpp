class DynamicArray {
private:
    int* data;      // Pointer to the underlying array
    int size;       // Number of elements currently stored
    int capacity;   // Total capacity of the array
public:

    // Constructor: initialize empty array with given capacity > 0
    explicit DynamicArray(int initialCapacity)
        : data(nullptr), size(0), capacity(initialCapacity)
    {
        if (initialCapacity <= 0) {
            throw std::runtime_error("Capacity must be > 0");
        }
        data = new int[capacity];
    }

    // Copy constructor (Rule of Three)
    DynamicArray(const DynamicArray& other)
        : data(new int[other.capacity]),
          size(other.size),
          capacity(other.capacity)
    {
        for (int i = 0; i < size; ++i) {
            data[i] = other.data[i];
        }
    }

    // Copy assignment operator (Rule of Three)
    DynamicArray& operator=(const DynamicArray& other) {
        if (this == &other) {
            return *this; // self-assignment guard
        }

        // 1) Allocate new memory
        int* newData = new int[other.capacity];

        // 2) Copy elements
        for (int i = 0; i < other.size; ++i) {
            newData[i] = other.data[i];
        }

        // 3) Release old memory
        delete[] data;

        // 4) Assign new state
        data = newData;
        size = other.size;
        capacity = other.capacity;

        return *this;
    }

    // Destructor (Rule of Three)
    ~DynamicArray() {
        delete[] data;
    }

    // Get element at index i (assume index is valid according to problem)
    int get(int i) const {
        // In real code we’d check: if (i < 0 || i >= size) ...
        return data[i];
    }

    // Set element at index i to n (assume index is valid)
    void set(int i, int n) {
        // In real code we’d check index bounds
        data[i] = n;
    }

    // Push an element at the end of the array
    void pushback(int n) {
        if (size == capacity) {
            resize(); // double capacity if full
        }
        data[size] = n;
        ++size;
    }

    // Pop and return the last element (assume array is non-empty)
    int popback() {
        // In real code: if (size == 0) throw...
        --size;           // move "end" one step to the left
        return data[size]; // return the old last element
    }

    // Double the capacity of the array
    void resize() {
        int newCapacity = capacity * 2;
        int* newData = new int[newCapacity];

        // Copy existing elements
        for (int i = 0; i < size; ++i) {
            newData[i] = data[i];
        }

        // Release old memory
        delete[] data;

        // Update pointer and capacity
        data = newData;
        capacity = newCapacity;
    }

    // Return current number of elements
    int getSize() const {
        return size;
    }

    // Return current capacity
    int getCapacity() const {
        return capacity;
    }
};
