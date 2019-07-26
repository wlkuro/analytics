import { Router } from 'express'

import users from './users'
import base from './base'
import senmon from './senmon'

const router = Router()

// Add USERS Routes
router.use(users)

// Add USERS Routes
router.use(base)

// Add USERS Routes
router.use(senmon)


export default router
