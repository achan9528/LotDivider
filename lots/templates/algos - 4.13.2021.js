// TwoSum (LeetCode)
// Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
// You may assume that each input would have exactly one solution, and you may not use the same element twice.
// You can return the answer in any order.

// Example 1:

// Input: nums = [2,7,11,15], target = 9
// Output: [0,1]
// Output: Because nums[0] + nums[1] == 9, we return [0, 1].
// Example 2:

// Input: nums = [3,2,4], target = 6
// Output: [1,2]
// Example 3:

// Input: nums = [3,3], target = 6
// Output: [0,1]

// Constraints:

// 2 <= nums.length <= 103
// -109 <= nums[i] <= 109
// -109 <= target <= 109
// Only one valid answer exists.

/**
 * @param {number[]} nums
 * @param {number} target
 * @return {number[]}
 */
var twoSum = function (nums, target) {
    // for each number in the nums array, see if there
    // are any other numbers which pair with such that their sum
    // equals the target
    for (let i = 0; i < nums.length; i++) {
        for (let n = 0; n < nums.length; n++) {
            // if n does not equal i, check to see if the sum
            // is equal to the target value
            if (n != i) {
                if (nums[i] + nums[n] == target) {
                    return [i, n];
                }
            }
        }
    }
    return -1
};

nums1 = [2, 7, 11, 15]
target1 = 9

nums2 = [3, 3]
target2 = 6

nums3 = [3, 2, 4]
target3 = 6

console.log(twoSum(nums1, target1));
console.log(twoSum(nums2, target2));
console.log(twoSum(nums3, target3));

// Add Two Numbers (LeetCode)
// You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.
// You may assume the two numbers do not contain any leading zero, except the number 0 itself.

// Input: l1 = [2,4,3], l2 = [5,6,4]
// Output: [7,0,8]
// Explanation: 342 + 465 = 807.

// Input: l1 = [0], l2 = [0]
// Output: [0]

// Input: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
// Output: [8,9,9,9,0,0,0,1]

/**
 * Definition for singly-linked list.
 * function ListNode(val, next) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.next = (next===undefined ? null : next)
 * }
 */
/**
 * @param {ListNode} l1
 * @param {ListNode} l2
 * @return {ListNode}
 */
var addTwoNumbers = function (l1, l2) {
    // read the values as a string and then parse the Int
    // read the values and then sum them. the fact that they are in
    // reverse order actually helps because it becomes like adding 
    // values by hand

    // for each value in each list, go one by one summing the parts
    // if there is a remainder, make sure to add it to the next sum
    // over. In addition, multiply each value by the digit it represents
    // e.g. second number you will multiply by a value of 10 because it
    // is in the 10's position

    // while there is a value at the next node
    let multiplier = 0;
    let currentNode = l1
    let l1Num = 0;
    while (currentNode.val) {
        l1Num += currentNode.value * (10 ** multiplier);
        currentNode = currentNode.next;
        multiplier++;
    }

    multiplier = 0;
    let currentNode = l2
    let l2Num = 0;
    while (currentNode.val) {
        l2Num += currentNode.value * (10 ** multiplier);
        currentNode = currentNode.next;
        multiplier++;
    }

    multiplier = 0;
    let sum = l1Num + l2Num;
    let newList = []
    while (sum > 0) {
        let digit = sum % 10;
        sum -= digit * (10 ** multiplier);
        multiplier++;
        newList.push(newNode(digit));
    }

    for (let i = 0; i < newList.length; i++) {
        if (i != newList.length - 1) {
            newList[i].next = newList[i + 1];
        }
    }

    return newList;
};

