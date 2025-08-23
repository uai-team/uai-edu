/**
 * 存储localStorage
 * @param expireTime 单位：分
 */
export function setStorage(name, content, expireTime) {
  if (!name) {
    return
  }
  let params = JSON.stringify(content)
  if (expireTime) {
    expireTime = Date.now() + expireTime * 1000 * 60
    params = JSON.stringify({ content: content, expireTime: expireTime })
  }
  window.localStorage.setItem(name, params)
}

/**
 * 获取localStorage
 */
export function getStorage(name) {
  if (!name) {
    return
  }
  let data = window.localStorage.getItem(name)
  if (!data) {
    return null
  }
  data = JSON.parse(data)
  if (data) {
    if (data.expireTime && data.expireTime > 0) {
      if (data.expireTime > Date.now()) {
        return data.content
      }
      window.localStorage.removeItem(name)
      return null
    }
    return data
  }
  return null
}

export function setStorageUser(content) {
  window.localStorage.setItem("UAI_EDU_USER", JSON.stringify(content))
}

export function getStorageUser() {
  let data = window.localStorage.getItem("UAI_EDU_USER")
  return JSON.parse(data)
}

export function removeStorageUser() {
  window.localStorage.removeItem("UAI_EDU_USER")
}

/**
 *
 * @param name
 * @param expireTime 单位：分
 */
export function setSessionStorage(name, content, expireTime) {
  if (!name) {
    return
  }
  let params = JSON.stringify(content)
  if (expireTime) {
    expireTime = Date.now() + expireTime * 1000 * 60
    params = JSON.stringify({ content: content, expireTime: expireTime })
  }
  window.sessionStorage.setItem(name, params)
}

/**
 * 获取sessionStorage
 */
export function getSessionStorage(name) {
  if (!name) {
    return null
  }
  let data = window.sessionStorage.getItem(name)
  if (!data) {
    return null
  }
  data = JSON.parse(data)
  if (data) {
    if (data.expireTime && data.expireTime > 0) {
      if (data.expireTime > Date.now()) {
        return data.content
      }
      window.sessionStorage.removeItem(name)
      return null
    }
    return data
  }
  return null
}
