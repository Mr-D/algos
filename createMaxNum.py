'''
Given two arrays of length m and n with digits 0-9 representing two numbers. Create the maximum number of length k <= m + n from digits of the two. The relative order of the digits from the same array must be preserved. Return an array of the k digits. You should try to optimize your time and space complexity.

Example 1:
nums1 = [3, 4, 6, 5]
nums2 = [9, 1, 2, 5, 8, 3]
k = 5
return [9, 8, 6, 5, 3]

Example 2:
nums1 = [6, 7]
nums2 = [6, 0, 4]
k = 5
return [6, 7, 6, 0, 4]

Example 3:
nums1 = [3, 9]
nums2 = [8, 9]
k = 3
return [9, 8, 9]
'''


class Node():
	def __init__(self, val, idx, next=None):
		self.val = val
		self.idx = idx
		self.next = next


class NumStruct():
	def __insert_max(self, val_idx):
		if val_idx >= self.len:
			return

		val = self.nums[val_idx]
		node = Node(val, val_idx)
		next_node = self.max_idx

		if not next_node or next_node.val < val:
			self.max_idx = node
			return

		while True:
			if next_node.next is None or next_node.next.val < val:
				next_node.next = node
				break
			next_node = next_node.next

	def __init__(self, nums, initial_len):
		self.nums = nums
		self.len = len(nums)
		self.max_idx = None

		self.start = 0
		self.end = initial_len
		for i in range(0, initial_len):
			self.__insert_max(i)

		next_node = self.max_idx
		while next_node:
			# print "(%d %d)" % (next_node.val, next_node.idx)
			next_node = next_node.next

	def get_max(self):
		if not self.max_idx:
			return -1, -1, -1
		return self.max_idx.val, self.max_idx.idx, self.len - self.max_idx.idx - 1

	def pop(self):
		if not self.max_idx:
			raise Exception('not possible')

		self.start = self.max_idx.idx + 1
		self.max_idx = self.max_idx.next

		if self.end < self.len:
			self.__insert_max(self.end)
			self.end += 1

	def restruct(self, remains):
		new_end = self.len - remains + 1
		if self.end == new_end:
			return

		self.end = new_end
		re_start, re_end = self.start, self.end

		node = self.max_idx
		pre = None
		while node:
			if node.idx >= new_end:
				if pre:
					pre.next = None
				else:
					self.max_idx = None

				break
			re_start = node.idx + 1
			pre = node
			node = node.next

		for i in range(re_start, re_end):
			self.__insert_max(i)


class Solution(object):
	def doMaxNumber(self, nums1, start1, end1, nums2, start2, end2, k):
		len1, len2 = len(nums1), len(nums2)
		build_len1 = len1 - ((k - len2) if (k - len2) > 0 else 0)
		nums_struct1 = NumStruct(nums1, build_len1 + 1)
		build_len2 = len2 - ((k - len1) if (k - len1) > 0 else 0)
		nums_struct2 = NumStruct(nums2, build_len2 + 1)

		result = [-1] * k
		cursor = 0

		while True:
			# print result
			top1, idx1, left1 = nums_struct1.get_max()
			top2, idx2, left2 = nums_struct2.get_max()

			result[cursor] = max(top1, top2)
			cursor += 1

			if cursor == k:
				break

			if top1 > top2:
				nums_struct1.pop()
				remain2 = k - cursor - left1
				nums_struct2.restruct(remain2)
			elif top2 > top1:
				nums_struct2.pop()
				remain1 = k - cursor - left2
				nums_struct1.restruct(remain1)
			else:
				# top2 == top1
				new_k = k - cursor - 1 - (left1 + left2)
				# if left1 + left2 < k - cursor - 1:
				if new_k > 0:
					cp_nums1 = nums1[nums_struct1.start:idx1]
					cp_nums2 = nums2[nums_struct2.start:idx2]
					solution = Solution()
					sub_k = solution.maxNumber(cp_nums1, cp_nums2, new_k)
					for v in sub_k:
						result[cursor] = v
						cursor += 1

					result[cursor] = top1
					cursor += 1

					nums_struct1.pop()
					nums_struct2.pop()

				else:
					# just get any of two
					nums_struct1.pop()
					remain2 = k - cursor - left1
					nums_struct2.restruct(remain2)

		return result


	def maxNumber(self, nums1, nums2, k):
		array = self.doMaxNumber(nums1, 0, len(nums1), nums2, 0, len(nums2), k)
		print array
		return array


solution = Solution()
solution.maxNumber([8, 0, 4, 2, 1], [1, 2, 3, 4, 5], 7)
solution.maxNumber([0, 2, 7, 6, 8, 8, 8, 4, 1], [1, 9], 7)
solution.maxNumber([1, 1, 1, 1, 1, 1, 7, 0, 0], [1, 2, 3, 4, 5], 7)
solution.maxNumber([1, 2, 7, 0, 5, 4, 1], [], 7)
print solution.maxNumber([6, 7], [6, 0, 4], 5)

