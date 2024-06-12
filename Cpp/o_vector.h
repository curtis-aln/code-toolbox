#pragma once

#include <ranges>
#include <array>
#include <vector>


/*
- Optimize iterator implementation for better performance, possibly by caching the last active index.
- Implement boundary checks in the at method for safer object retrieval.
- Enhance the efficiency of adding and removing objects, possibly by avoiding linear searches.
- Consider alternative data structures such as linked lists or hash maps for better performance with large datasets.
- Improve error handling to provide more informative feedback in cases of container overflow or other errors.
 */


// add this as a public parent struct to the Obj class/structure
struct o_vec_object
{
    unsigned o_vec_index = 0;
    bool active = true;

    o_vec_object() = default;
};


template <class Obj, std::size_t N>
class o_vector
{
public:
    // this tracks the amount of objects there are active
    int active_objs = 0;

private:
    // this array contains all the items and is never directly modified
    std::array<Obj*, N> array{};

    // this tracks the actual initilised and implemented Objects being used
    unsigned array_size = 0;

    // this vectorPtr stores all the actual objects on the heap, they are never modified or removed from. only added to
    std::vector<Obj> objectStore{};


private:
    // Iterator class definition
    class Iterator
    {
    public:
        using iterator_category = std::forward_iterator_tag;
        using value_type = Obj*;
        using difference_type = std::ptrdiff_t;
        using pointer = Obj*;
        using reference = Obj&;

        explicit Iterator(o_vector* vec = nullptr, const unsigned index = 0) : vectorPtr(vec), currentIndex(index) {}
        Iterator() : vectorPtr(nullptr) {}

        Iterator& operator++()
        {
            do { ++currentIndex; } while (currentIndex < vectorPtr->array.size() && !vectorPtr->array[currentIndex]->active);
            return *this;
        }

        pointer operator*()   const { return vectorPtr->array[currentIndex]; }
        pointer operator->()  const { return vectorPtr->array[currentIndex]; }


        bool operator==(const Iterator& other) const { return currentIndex == other.currentIndex; }
        bool operator!=(const Iterator& other) const { return !(*this == other); }

    private:
        o_vector* vectorPtr;
        unsigned currentIndex = 0;
    };


    unsigned getFirstAvalableIteration() const
    {
        unsigned currentIndex = 0;
        while (currentIndex < N && !array[currentIndex]->active)
            ++currentIndex;
        return currentIndex;
    }


public:
    explicit o_vector() { objectStore.reserve(N); }

    [[nodiscard]] Iterator begin() const { return Iterator(const_cast<o_vector*>(this), getFirstAvalableIteration()); }
    [[nodiscard]] Iterator end() const { return Iterator(nullptr, static_cast<unsigned>(N)); }
    [[nodiscard]] unsigned size() const { return active_objs; }



    // used to initilise items inside of objectStore.
    void emplace(Obj item)
    {
        objectStore.emplace_back(item);
        array[array_size] = &objectStore[array_size];
        ++array_size;
        ++active_objs;
    }


    Obj* at(const unsigned i) { return array[i]; }


    Obj* add()
    {
        if (size() >= array_size)
            return nullptr;

        for (size_t i{ 0 }; i < array_size; ++i)
        {
            if (!array[i]->active)
            {
                array[i]->active = true;
                ++active_objs;
                return array[i];
            }
        }

        return nullptr;
    }


    void remove(Obj* obj) { if (obj->active) remove(obj->o_vec_index); }
    void remove(const unsigned vector_index)
    {
        if (array[vector_index]->active)
        {
            array[vector_index]->active = false;
            --active_objs;
        }
    }
};
